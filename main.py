import base64
import json
import re

# 从文件读取节点链接和IP列表
with open('v2.txt', 'r') as f:
    sample_node = f.read().replace('\n', '').strip()

with open('ip.txt', 'r') as f:
    giplist = f.read().strip().splitlines()

# 识别请求头
supported_prefixes = ["vmess://", "vless://", "trojan://"]

if not any(sample_node.startswith(prefix) for prefix in supported_prefixes):
    print("仅支持vmess、vless和trojan的节点分享链接！")
else:
    nodes = []
    if sample_node.startswith("vmess://"):
        try:
            # 解码vmess链接
            node_data = base64.b64decode(sample_node[8:]).decode('utf-8')
            config = json.loads(node_data)  # 转换为字典

            # 按顺序替换add字段
            for ip in giplist:
                config["add"] = ip  # 替换add字段
                
                # 重新编码成vmess链接
                new_node_data = base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')
                nodes.append("vmess://" + new_node_data + '\n')

        except Exception as error:
            print("处理vmess链接时出现错误：", str(error))
    
    elif sample_node.startswith("vless://") or sample_node.startswith("trojan://"):
        # 处理vless和trojan链接
        try:
            re_pattern = r'@([^:]+):'
            node_host = re.search(re_pattern, sample_node).group(1)

            # 按顺序替换IP
            for ip in giplist:
                if sample_node.startswith("vless://"):
                    new_node = re.sub(r'@.*?:', f'@{ip}:', sample_node)
                else:  # trojan
                    new_node = re.sub(r'@.*?:', f'@{ip}:', sample_node)
                
                nodes.append(new_node + '\n')

        except Exception as error:
            print("处理vless或trojan链接时出现错误：", str(error))

    # 将输出保存到ray.txt
    with open('ray.txt', 'w') as f:
        f.writelines(nodes)

    print("节点链接已成功输出到ray.txt")
