import requests

def fetch_list(url):
    # 关键：设置连接+读取超时，超过20秒直接报错退出，不会无限卡死
    resp = requests.get(url, timeout=(10, 20))
    resp.raise_for_status()
    return resp.text.splitlines()

def main():
    sources = []
    with open("sources.txt","r",encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                sources.append(line)

    unique_rules = set()
    for url in sources:
        print(f"✅ 已处理: {url}")
        try:
            lines = fetch_list(url)
        except Exception as e:
            print(f"⚠️ 获取 {url} 失败，跳过该源: {e}")
            continue
        cnt = 0
        for l in lines:
            strip_l = l.strip()
            if not strip_l or strip_l.startswith("#"):
                continue
            unique_rules.add(strip_l)
            cnt +=1
        print(f"有效规则 {cnt} 条")

    print(f"🎉 合并完成，共 {len(unique_rules)} 条唯一规则")
    with open("merged_blacklist.txt","w",encoding="utf-8") as f:
        for rule in sorted(unique_rules):
            f.write(rule + "\n")

if __name__ == "__main__":
    main()
