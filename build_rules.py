#!/usr/bin/env python3
"""Rebuild Loon rule files from blackmatrix7/ios_rule_script (via GitHub tree API):
   - cn-direct.list : domestic apps/ecosystems + ChinaMax, policy DIRECT (user picks in Loon)
   - ai.list        : all AI services, policy = proxy group in Loon
   - apple.list     : all Apple services, policy DIRECT in Loon
Excludes (user already added them separately): WeChat, BaiDuTieBa, DouYin, AliPay, GaoDe.
Safety: if a rebuilt file falls below its threshold, keep the old file and exit nonzero.
"""
import io, json, sys, urllib.request
from datetime import datetime, timezone, timedelta

BASE = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon/"
import sys as _s
OUTDIR = _s.argv[1].rstrip("/") + "/" if len(_s.argv) > 1 else "./"
CST = timezone(timedelta(hours=8))

CN_APPS = [("腾讯系", "Tencent"), ("阿里系·淘宝天猫", "Alibaba"), ("京东", "JingDong"),
        ("拼多多", "Pinduoduo"), ("闲鱼", "XianYu"), ("美团", "MeiTuan"), ("饿了么", "Eleme"),
        ("快手", "KuaiShou"), ("哔哩哔哩", "BiliBili"), ("小红书", "XiaoHongShu"), ("微博", "Weibo"),
        ("知乎", "Zhihu"), ("豆瓣", "DouBan"), ("百度", "Baidu"), ("滴滴", "DiDi"),
        ("铁路12306", "12306"), ("携程", "XieCheng"), ("爱奇艺", "iQIYI"), ("优酷", "Youku"),
        ("腾讯视频", "TencentVideo"), ("网易云音乐", "NetEaseMusic"), ("酷狗酷我", "KugouKuwo"),
        ("网易系", "NetEase"), ("新浪", "Sina"), ("UC浏览器", "UC"), ("钉钉", "DingTalk"),
        ("字节系", "ByteDance"), ("华为", "Huawei"), ("小米", "XiaoMi"), ("OPPO", "OPPO"),
        ("vivo", "Vivo"), ("魅族", "MeiZu"), ("联想", "Lenovo"), ("金山", "Kingsoft"),
        ("虎牙", "HuYa"), ("斗鱼", "Douyu"), ("虎扑", "Hupu"), ("简书", "JianShu"),
        ("CSDN", "CSDN"), ("掘金", "JueJin"), ("TapTap", "TapTap"), ("NGA", "NGA"),
        ("AcFun", "AcFun"), ("唯品会", "VipShop"), ("苏宁易购", "SuNing"), ("当当", "DangDang"),
        ("转转", "ZhuanZhuan"), ("菜鸟", "CaiNiao"), ("顺丰", "SFExpress"), ("盒马", "HeMa"),
        ("快递100", "KuaiDi100"), ("同程旅行", "TongCheng"), ("飞猪", "FeiZhu"), ("大麦", "DaMai"),
        ("中国国航", "AirChina"), ("乐视", "LeTV"), ("PPTV", "PPTV"), ("芒果TV", "HunanTV"),
        ("央视", "CCTV"), ("咪咕", "Migu"), ("迅雷", "Xunlei"), ("科大讯飞", "iFlytek"),
        ("酷安", "Coolapk"), ("什么值得买", "SMZDM"), ("搜狐", "Sohu"), ("凤凰网", "FengHuangWang"),
        ("东方财富", "EastMoney"), ("雪球", "XueQiu"), ("中国银行", "BOC"), ("建设银行", "CCB"),
        ("工商银行", "ICBC"), ("招商银行", "CMB"), ("交通银行", "BOCOM"), ("邮储银行", "PSBC"),
        ("光大银行", "CEB"), ("广发银行", "CGB"), ("平安", "PingAn"), ("银联", "UnionPay"),
        ("360", "360"), ("58同城", "58TongCheng"), ("前程无忧", "51Job"), ("政府网站", "GovCN"),
        ("中国移动", "ChinaMobile"), ("中国电信", "ChinaTelecom"), ("中国联通", "ChinaUnicom"),
        ("安居客", "Anjuke"), ("搜房", "SouFang"), ("115网盘", "115"), ("蓝奏云", "LanZouYun"),
        ("Gitee", "Gitee"), ("猿辅导", "YuanFuDao"), ("学而思", "XueErSi"), ("知网", "CNKI"),
        ("七牛云", "QiNiuYun"), ("又拍云", "UPYun"), ("深度Deepin", "Deepin"), ("蘑菇街", "Mogujie"),
        ("国内全量ChinaMax", "ChinaMax")]
CN_EXTRA = [("拼多多·实测补充", ["DOMAIN-SUFFIX,pinduoduo.net"])]  # from user's Loon log 2026-11-05

AI_APPS = [("OpenAI·ChatGPT", "OpenAI"), ("Claude", "Claude"), ("Anthropic", "Anthropic"),
        ("Gemini", "Gemini"), ("Bard", "BardAI"), ("Copilot", "Copilot"), ("必应Bing", "Bing"),
        ("Civitai", "Civitai")]
AI_EXTRA = [("人工补充·源仓库暂无", ["DOMAIN-SUFFIX,grok.com", "DOMAIN-SUFFIX,x.ai",
        "DOMAIN-SUFFIX,perplexity.ai", "DOMAIN-SUFFIX,poe.com", "DOMAIN-SUFFIX,midjourney.com",
        "DOMAIN-SUFFIX,huggingface.co", "DOMAIN-SUFFIX,character.ai", "DOMAIN-SUFFIX,mistral.ai",
        "DOMAIN-SUFFIX,suno.com", "DOMAIN-SUFFIX,elevenlabs.io"])]

APPLE_EXTRA = [("苹果推送·人工补充", ["DOMAIN-SUFFIX,push.apple.com"])]
ROCM_AI_URL = "https://raw.githubusercontent.com/RocM301/Apple-Rule/refs/heads/main/Apple-AI.list"

APPLE_APPS = [("苹果服务总集", "Apple"), ("App Store", "AppStore"), ("iCloud", "iCloud"), ("Apple ID", "AppleID"),
        ("苹果媒体服务", "AppleMedia"), ("Apple Music", "AppleMusic"), ("Apple TV", "AppleTV"),
        ("Apple News", "AppleNews"), ("苹果邮件", "AppleMail"), ("苹果开发者", "AppleDev"),
        ("固件更新", "AppleFirmware"), ("苹果硬件服务", "AppleHardware"), ("苹果代理服务", "AppleProxy"),
        ("iCloud专用中继", "iCloudPrivateRelay")]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cn-rules-builder/2.0"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")

def main():
    tree = json.loads(fetch("https://api.github.com/repos/blackmatrix7/ios_rule_script/git/trees/master?recursive=1"))["tree"]
    dirfiles = {}
    for t in tree:
        p = t["path"]
        if p.startswith("rule/Loon/") and p.endswith(".list"):
            parts = p.split("/")
            if len(parts) == 4:
                dirfiles.setdefault(parts[2], []).append(parts[3])

    def get_set(name):
        out = []
        for fn in sorted(dirfiles.get(name, [])):
            for ln in fetch(BASE + name + "/" + fn).splitlines():
                ln = ln.strip()
                if not ln or ln.startswith("#"):
                    continue
                if "," not in ln:  # bare domain line in _Domain lists
                    ln = "DOMAIN-SUFFIX," + ln.lstrip(".")
                out.append(ln)
        return out

    def build(apps, extras, outfile, title, note, threshold):
        seen, sections, total = set(), [], 0
        for label, name in apps:
            lines = []
            for ln in get_set(name):
                if ln not in seen:
                    seen.add(ln)
                    lines.append(ln)
            if lines:
                sections.append((label, lines))
                total += len(lines)
        for label, raw in extras:
            lines = [ln for ln in raw if ln not in seen]
            for ln in lines:
                seen.add(ln)
            if lines:
                sections.append((label, lines))
                total += len(lines)
        if total < threshold:
            print("ABORT %s: only %d rules (< %d), keeping old file" % (outfile, total, threshold))
            return False
        now = datetime.now(CST).strftime("%Y-%m-%d %H:%M CST")
        lines = ["# " + title, "# " + note,
                 "# 服务器每周自动更新，上次更新：%s，共 %d 个分组、%d 条规则" % (now, len(sections), total), ""]
        for label, ls in sections:
            lines.append("# ===== %s (%d) =====" % (label, len(ls)))
            lines.extend(ls)
            lines.append("")
        path = OUTDIR + outfile
        try:
            old = io.open(path, encoding="utf-8").read()
            io.open(path + ".bak", "w", encoding="utf-8").write(old)
        except FileNotFoundError:
            pass
        io.open(path, "w", encoding="utf-8").write("\n".join(lines))
        print("OK: %s - %d sections, %d rules" % (outfile, len(sections), total))
        return True

    ok = True
    ok &= build(CN_APPS, CN_EXTRA, "cn-direct.list",
                "国内常用 App 直连规则（Loon 远程规则版，策略在 Loon 里选 DIRECT）",
                "数据来源：blackmatrix7/ios_rule_script（经 luestr/ShuntRules 索引整理），已剔除微信/贴吧/抖音/支付宝/高德", 4000)
    ai_extras = list(AI_EXTRA)
    try:
        rocm = []
        for ln in fetch(ROCM_AI_URL).splitlines():
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                if "," not in ln:
                    ln = "DOMAIN-SUFFIX," + ln.lstrip(".")
                rocm.append(ln)
        if rocm:
            ai_extras.append(("苹果智能Apple Intelligence·RocM301", rocm))
    except Exception as e:
        print("WARN: RocM301 Apple-AI fetch failed:", e)
    ok &= build(AI_APPS, ai_extras, "ai.list",
                "AI 服务规则（Loon 远程规则版，策略在 Loon 里选你的节点策略组）",
                "数据来源：blackmatrix7/ios_rule_script + 人工补充 + 苹果智能(RocM301/Apple-Rule)", 50)
    ok &= build(APPLE_APPS, APPLE_EXTRA, "apple.list",
                "苹果全家桶规则（Loon 远程规则版，策略在 Loon 里选 DIRECT）",
                "数据来源：blackmatrix7/ios_rule_script（AppleDaily 是香港苹果日报新闻，已排除）", 200)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
