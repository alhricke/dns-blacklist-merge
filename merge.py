import requests
import re

# 输入源列表文件
SOURCE_FILE = "sources.txt"
# 输出合并后的黑名单
OUTPUT_FILE = "merged_blacklist.txt"

# 匹配域名正则
domain_pattern = re.compile(r"([a-zA-Z0-9][a-zA-Z0-9\.\-]*\.[a-zA-Z]{2,})")

def main():
    domains = set()
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for url in urls:
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            text = resp.text
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = domain_pattern.search(line)
                if match:
                    domain = match.group(1).lower()
                    domains.add(domain)
            print(f"✅ 已处理: {url}")
        except Exception as e:
            print(f"❌ 下载失败 {url} : {e}")

    # 排序后写入文件
    sorted_domains = sorted(list(domains))
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted_domains))
    print(f"\n🎉 合并完成，共 {len(sorted_domains)} 个唯一域名")

if __name__ == "__main__":
    main()
