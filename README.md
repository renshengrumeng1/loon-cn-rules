# Loon 规则集（自用整理）

四个远程规则文件，配合 Loon 使用。每周从源仓库自动重建更新，不依赖任何 VPS。

## 1. 国内直连 cn-direct.list

```
https://raw.githubusercontent.com/renshengrumeng1/loon-cn-rules/main/cn-direct.list
```

- 策略选 **DIRECT**；位置放在去广告规则集下面、其他分流上面、FINAL 之前
- 95 个国内 App / 生态 + ChinaMax 全量，共约 13.8 万条
- 未含微信、百度贴吧、抖音、支付宝、高德（站长已单独添加）

## 2. AI 服务 ai.list

```
https://raw.githubusercontent.com/renshengrumeng1/loon-cn-rules/main/ai.list
```

- 策略选**节点策略组**（走代理）
- OpenAI/ChatGPT、Claude、Gemini、Copilot、必应、Civitai，外加人工补充的 Grok、Perplexity、Poe、Midjourney、HuggingFace 等
- 苹果智能 Apple Intelligence（源：[RocM301/Apple-Rule](https://github.com/RocM301/Apple-Rule)）——锁区服务，必须走支持地区节点，故并入本文件随代理走

## 3. 苹果全家桶 apple.list

```
https://raw.githubusercontent.com/renshengrumeng1/loon-cn-rules/main/apple.list
```

- 策略选 **DIRECT**（苹果服务国内直连最快，iCloud 为云上贵州运营）
- Apple 总集、iCloud、Apple ID、媒体服务、Music、TV、News、邮件、开发者、固件更新等全套（AppleDaily 是香港苹果日报新闻，已排除）

## 4. IP 归属地 anti-ip.list

```
https://raw.githubusercontent.com/renshengrumeng1/loon-cn-rules/main/anti-ip.list
```

- 策略选**你想让归属地显示的节点组**（如某个省的节点/家宽线）
- 微博、抖音、小红书、知乎、贴吧、B站等会显示 IP 归属地的 App：只把定位接口（233 条）送代理，其余流量不动；文件内已标注的 REJECT（定位/HTTPDNS 拦截）与 DIRECT（视频 CDN）按标注执行
- 数据来源：[SunsetMkt/anti-ip-attribution](https://github.com/SunsetMkt/anti-ip-attribution)
- 免责声明（源项目）：本项目仅用于学习交流，请在遵守所在地法律法规的前提下使用。本项目记录的 API 域名地址信息可以被任何人通过开发人员工具获取，没有经过逆向工程或网络攻击，不构成入侵计算机系统。请不要在中华人民共和国境内使用此项目。

## 数据来源

规则源：[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)（经 [luestr/ShuntRules](https://github.com/luestr/ShuntRules) 索引整理）。
