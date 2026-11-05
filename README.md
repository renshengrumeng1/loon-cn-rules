# Loon 国内直连规则（cn-direct）

国内常用 App 与国内网站的直连规则集（策略 DIRECT），远程规则格式，配合 Loon 使用。

## 在 Loon 里添加

远程规则地址（二选一，内容相同）：

```
https://raw.githubusercontent.com/renshengrumeng1/loon-cn-rules/main/cn-direct.list
https://ql.pokoc.com:8444/sub/cn-direct.list
```

添加时策略选 **DIRECT**，位置放在去广告规则集**下面**、其他分流规则上面、**FINAL 之前**（Loon 自上而下先命中先生效）。

## 内容

- 95 个国内 App / 生态规则（腾讯、阿里、京东、拼多多、美团、快手、B站、小红书、银行、运营商等）
- ChinaMax 国内全量（域名 + IP 段）
- 共 13.8 万条（以文件头注释为准）

未包含：微信、百度贴吧、抖音、支付宝、高德（站长已单独添加同类规则，避免重复）。

## 数据来源与更新

- 规则源：[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)（经 [luestr/ShuntRules](https://github.com/luestr/ShuntRules) 索引）
- 服务器每周从源仓库自动重建并同步到本仓库；拼多多 `pinduoduo.net` 为按实测日志人工补入
