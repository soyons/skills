---
name: kpl_api
description: >
  KPL（看盘龙）A股量化数据接口。覆盖龙虎榜、实时行情、个股盘口/分时/大单、K线（日/周/月/历史/涨停）、
  概念板块热点、指数走势、资讯评论、用户自选股，以及日志上报（防风控）。
  触发关键词：KPL、看盘龙、龙虎榜、LongHuBang、涨停、跌停、炸板、盘口、五档、分时、大单、
  K线、日线、周线、月线、板块、题材、概念、热点、指数、行情、人气股、资讯、评论、
  自选股、防风控、模拟登录。
metadata:
  openclaw:
    os: ["darwin", "linux"]
    requires:
      bins: ["python3"]
---

# KPL API Skill

## When To Use

用户出现以下任一意图时触发本技能：

- 查询龙虎榜数据（榜单列表、个股上榜明细、涨停跌停炸板统计）
- 查询实时行情（大盘指数、市场情绪、全球指数、人气股、盯盘、现货数据）
- 查询个股数据（盘口五档、分时走势、实时涨跌、大单趋势、所属板块、消息公告）
- 查询K线（当日/历史/大单/涨停/区间，支持日线/周线/月线）
- 查询概念板块（热点题材、概念直播、板块分时、板块排名、子板块、成分股）
- 查询指数数据（分时走势、盘口、成交量、上级板块、大盘走势）
- 查询资讯评论（资讯首页、精选列表、专栏、焦点消息、主题状态、评论列表）
- 用户相关（权限查询、委托通知、自选股刷新、个股文章标题）
- 防风控（模拟正常用户使用行为、登录上报、浏览上报）

## Preconditions

1. `skills/kpl_api/scripts/kpl_api.py` 和 `skills/kpl_api/scripts/call_kpl.py` 存在。
2. Python 环境已安装 `requests` 库。
3. `TOKEN`、`USER_ID`、`DEVICE_ID` 为敏感信息，禁止在回复中明文输出。

## Execution Steps

1. 根据用户意图从下方"方法完整参考"中选择对应方法。
2. 校验参数名、类型和默认值。
3. 使用统一调用命令：

```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "<method_name>" --kwargs '<json_object>'
```

无参数方法省略 `--kwargs`：

```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "<method_name>"
```

4. 解析 JSON 返回，提取核心字段（状态、代码、名称、价格、涨跌幅、成交、时间等）。
5. 返回数据过大时只输出摘要和关键字段。
6. 失败时返回：调用方法、脱敏错误信息、建议回退方法。

## 参数规范

| 参数类型 | 格式 | 示例 |
|---------|------|------|
| 股票代码 `stock_id` | 6位数字字符串 | `"300827"`、`"000001"` |
| 指数代码 `stock_id` | 带交易所前缀 | `"SH000001"`（上证）、`"SZ399001"`（深成） |
| 板块代码 `plate_id` | 6位数字字符串 | `"801070"` |
| 日期 | `YYYY-MM-DD` | `"2026-03-21"` |
| 分页索引 `index` | 整数，从0开始 | `0` |
| 每页条数 `st` | 整数 | `20`、`300` |
| K线周期 `type_` | 字符串 | `"d"`=日线 `"w"`=周线 `"m"`=月线 |
| 时间戳 `time` | 字符串，留空=最新 | `""`、`"1770557329"` |

## 方法完整参考（59个）

### 1. 龙虎榜（5个）

#### `lhb_update_list()`
获取龙虎榜更新日期等元信息。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "lhb_update_list"
```

#### `lhb_get_stock_list(index=0, st=300)`
获取龙虎榜股票列表。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `index` | int | `0` | 分页索引 |
| `st` | int | `300` | 数据条数 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "lhb_get_stock_list" --kwargs '{"index":0,"st":50}'
```

#### `lhb_top_title()`
获取龙虎榜顶部标题（涨停/跌停/炸板统计）。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "lhb_top_title"
```

#### `lhb_add(stock_id, date)`
查询个股龙虎榜明细。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码，如 `"000815"` |
| `date` | str | 是 | 日期 `YYYY-MM-DD` |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "lhb_add" --kwargs '{"stock_id":"000815","date":"2026-03-21"}'
```

#### `lhb_dongcai_state()`
获取龙虎榜东财数据状态。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "lhb_dongcai_state"
```

---

### 2. 主题/题材（2个）

#### `theme_info(theme_id)`
获取主题详情。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `theme_id` | str | 是 | 主题ID |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "theme_info" --kwargs '{"theme_id":"142"}'
```

#### `theme_plate_rank(zs_code)`
获取主题板块排名。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `zs_code` | str | 是 | 指数代码，如 `"801070"` |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "theme_plate_rank" --kwargs '{"zs_code":"801070"}'
```

---

### 3. 排行榜（2个）

#### `rank_ticai_stock_option()`
获取题材排行榜股票选项。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "rank_ticai_stock_option"
```

#### `rank_leading_times_option()`
获取领涨次数选项。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "rank_leading_times_option"
```

---

### 4. 实时行情（6个）

#### `hq_index_info(view="1,2,3,4,5,6,7,8,9,10,11")`
获取大盘行情总览。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `view` | str | `"1,2,3,4,5,6,7,8,9,10,11"` | 视图类型列表 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "hq_index_info"
```

#### `hq_home_dingpan()`
获取盯盘数据（涨停/跌停/炸板实时统计）。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "hq_home_dingpan"
```

#### `hq_market_mood()`
获取市场情绪指标。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "hq_market_mood"
```

#### `hq_global_index(view="1,2,3,4,5,6")`
获取全球主要指数。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `view` | str | `"1,2,3,4,5,6"` | 视图类型列表 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "hq_global_index"
```

#### `hq_popular_stocks(index=0, st=6, type_=2, order=1, pid_type=1)`
获取热门/人气股票排行。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `index` | int | `0` | 分页索引 |
| `st` | int | `6` | 每页条数 |
| `type_` | int | `2` | 数据类型 |
| `order` | int | `1` | 排序方式 |
| `pid_type` | int | `1` | 分类类型 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "hq_popular_stocks" --kwargs '{"index":0,"st":20}'
```

#### `hq_xian_huo(time="")`
获取现货/鲜活数据流。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `time` | str | `""` | 时间戳，留空取最新 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "hq_xian_huo"
```

---

### 5. 个股数据（7个）

#### `stock_bid(stock_id)`
获取股票买卖盘（五档行情）。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "stock_bid" --kwargs '{"stock_id":"300827"}'
```

#### `stock_pankou(stock_id, state=1)`
获取股票盘口数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `state` | int | `1` | 状态 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "stock_pankou" --kwargs '{"stock_id":"300827"}'
```

#### `stock_realdata(stock_id)`
获取股票实时数据（涨幅/量比/换手率等）。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "stock_realdata" --kwargs '{"stock_id":"300827"}'
```

#### `stock_trend(stock_id)`
获取股票分时走势。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "stock_trend" --kwargs '{"stock_id":"300827"}'
```

#### `stock_dadan_trend(stock_id, time="")`
获取股票大单分时走势。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `time` | str | `""` | 增量起始时间 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "stock_dadan_trend" --kwargs '{"stock_id":"300827"}'
```

#### `stock_featured_section(stock_id)`
获取个股所属板块/题材。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "stock_featured_section" --kwargs '{"stock_id":"300827"}'
```

#### `stock_message_bar(stock_id)`
获取个股消息/公告。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "stock_message_bar" --kwargs '{"stock_id":"300827"}'
```

---

### 6. K线数据（7个）

#### `kline_today(stock_id, type_="d", index=0, st=400)`
获取今日K线数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `type_` | str | `"d"` | `d`=日线 `w`=周线 `m`=月线 |
| `index` | int | `0` | 起始索引 |
| `st` | int | `400` | 数据条数 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "kline_today" --kwargs '{"stock_id":"300827","type_":"d"}'
```

#### `kline_zhangting(stock_id)`
获取K线涨停标记数据。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "kline_zhangting" --kwargs '{"stock_id":"300827"}'
```

#### `kline_dadan(stock_id, type_="d")`
获取K线大单数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `type_` | str | `"d"` | K线类型 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "kline_dadan" --kwargs '{"stock_id":"300827"}'
```

#### `kline_history(stock_id, type_="d", index=0, st=130, is_fs=1)`
获取历史K线数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `type_` | str | `"d"` | `d`=日线 `w`=周线 `m`=月线 |
| `index` | int | `0` | 起始索引 |
| `st` | int | `130` | 数据条数 |
| `is_fs` | int | `1` | 是否复权（1=复权） |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "kline_history" --kwargs '{"stock_id":"300827","type_":"d","st":60}'
```

#### `kline_history_dadan(stock_id, type_="d", index=0, st=131)`
获取历史大单K线数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `type_` | str | `"d"` | K线类型 |
| `index` | int | `0` | 起始索引 |
| `st` | int | `131` | 数据条数 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "kline_history_dadan" --kwargs '{"stock_id":"300827"}'
```

#### `kline_interval(stock_id, type_="d", index=0, st=47)`
获取K线区间统计数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `type_` | str | `"d"` | K线类型 |
| `index` | int | `0` | 起始索引 |
| `st` | int | `47` | 数据条数 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "kline_interval" --kwargs '{"stock_id":"300827"}'
```

#### `kline_history_zhangting(stock_id, index=0, st=20)`
获取历史涨停复盘数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `index` | int | `0` | 分页索引 |
| `st` | int | `20` | 每页条数 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "kline_history_zhangting" --kwargs '{"stock_id":"300827"}'
```

---

### 7. 概念/板块/指数（13个）

#### `conception_hotpoint()`
获取概念题材热点排行。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "conception_hotpoint"
```

#### `conception_zhibo()`
获取概念直播（实时异动）。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "conception_zhibo"
```

#### `conception_bk_fenshi(plate_id)`
获取板块分时走势。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plate_id` | str | 是 | 板块代码，如 `"801070"` |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "conception_bk_fenshi" --kwargs '{"plate_id":"801070"}'
```

#### `zhishu_trend(stock_id, time="")`
获取指数/板块分时走势。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 指数/板块代码 |
| `time` | str | `""` | 增量起始时间 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "zhishu_trend" --kwargs '{"stock_id":"801070"}'
```

#### `zhishu_pankou(stock_id)`
获取指数/板块盘口。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 指数/板块代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "zhishu_pankou" --kwargs '{"stock_id":"801070"}'
```

#### `zhishu_vol(stock_id, time="")`
获取指数/板块成交量换手增量。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 指数/板块代码 |
| `time` | str | `""` | 增量起始时间 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "zhishu_vol" --kwargs '{"stock_id":"801070"}'
```

#### `zhishu_parent_plate(stock_id)`
获取指数所属上级板块。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 指数/板块代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "zhishu_parent_plate" --kwargs '{"stock_id":"801070"}'
```

#### `zhishu_zs_trend(stock_id)`
获取大盘指数走势（上证/深成/创业板）。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 指数代码，如 `"SH000001"` |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "zhishu_zs_trend" --kwargs '{"stock_id":"SH000001"}'
```

#### `plate_tc_config()`
获取板块题材分类配置。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "plate_tc_config"
```

#### `plate_stock_tag(plate_id)`
获取板块成分股排行标签。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plate_id` | str | 是 | 板块代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "plate_stock_tag" --kwargs '{"plate_id":"801070"}'
```

#### `plate_info_qj(plate_id, r_start="", r_end="")`
获取板块区间涨跌信息。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `plate_id` | str | 必填 | 板块代码 |
| `r_start` | str | `""` | 区间开始日期 |
| `r_end` | str | `""` | 区间结束日期 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "plate_info_qj" --kwargs '{"plate_id":"801070"}'
```

#### `plate_son_info(plate_id)`
获取子板块列表。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plate_id` | str | 是 | 板块代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "plate_son_info" --kwargs '{"plate_id":"801070"}'
```

#### `plate_introduction(plate_id, stocks="")`
获取板块简介及成分股列表。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `plate_id` | str | 必填 | 板块代码 |
| `stocks` | str | `""` | 成分股代码，逗号分隔 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "plate_introduction" --kwargs '{"plate_id":"801070"}'
```

---

### 8. 资讯（6个）

#### `article_index(view="1,2,3,4")`
获取资讯首页板块列表。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `view` | str | `"1,2,3,4"` | 视图类型 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "article_index"
```

#### `article_sel_list(index=0, st=20, pre_index=0, select="0,1,2")`
获取精选资讯列表。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `index` | int | `0` | 分页索引 |
| `st` | int | `20` | 每页条数 |
| `pre_index` | int | `0` | 上一页索引 |
| `select` | str | `"0,1,2"` | 类型筛选 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "article_sel_list" --kwargs '{"index":0,"st":10}'
```

#### `article_column_list(index=0, st=10)`
获取专栏列表。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `index` | int | `0` | 分页索引 |
| `st` | int | `10` | 每页条数 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "article_column_list"
```

#### `article_column_info(column_id, index=0, st=20, pre_index=0, select="0,1,2")`
获取专栏详情。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `column_id` | str | 必填 | 专栏ID |
| `index` | int | `0` | 分页索引 |
| `st` | int | `20` | 每页条数 |
| `pre_index` | int | `0` | 上一页索引 |
| `select` | str | `"0,1,2"` | 类型筛选 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "article_column_info" --kwargs '{"column_id":"77"}'
```

#### `article_focus_msg(msg_id, type_=0)`
获取焦点/关注消息详情。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `msg_id` | str | 必填 | 消息ID |
| `type_` | int | `0` | 消息类型 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "article_focus_msg" --kwargs '{"msg_id":"Mzg5MzEyNzEwNQ=="}'
```

#### `article_theme_status(gid, g_type=2)`
获取主题新闻状态。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `gid` | str | 必填 | 主题ID |
| `g_type` | int | `2` | 主题类型 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "article_theme_status" --kwargs '{"gid":"35"}'
```

---

### 9. 评论（1个）

#### `comments_get(stock_id, type_=4, index=0, st=20, tsort=9, day="")`
获取评论列表。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票/主题ID |
| `type_` | int | `4` | 评论类型 |
| `index` | int | `0` | 分页索引 |
| `st` | int | `20` | 每页条数 |
| `tsort` | int | `9` | 排序方式 |
| `day` | str | `""` | 日期过滤 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "comments_get" --kwargs '{"stock_id":"142","type_":4}'
```

---

### 10. 用户（4个）

#### `user_permission(type_=33)`
获取用户权限（判断VIP等级）。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `type_` | int | `33` | 权限类型 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "user_permission"
```

#### `user_weituo_notify(stock_id)`
获取委托通知。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "user_weituo_notify" --kwargs '{"stock_id":"300827"}'
```

#### `user_select_stock_refresh(stock_id_list)`
刷新自选股行情。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id_list` | str | 是 | 股票代码列表，如 `"SH000001"` |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "user_select_stock_refresh" --kwargs '{"stock_id_list":"SH000001"}'
```

#### `user_stock_art_title(stock_id, type_=1)`
获取个股相关文章/公告标题。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `stock_id` | str | 必填 | 股票代码 |
| `type_` | int | `1` | 类型 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "user_stock_art_title" --kwargs '{"stock_id":"300827"}'
```

---

### 11. 日志上报/防风控（6个）

#### `log_user_login()`
上报用户登录。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "log_user_login"
```

#### `log_page_view(data_list, channel_id="0")`
上报页面浏览数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data_list` | str | 必填 | JSON格式浏览数据 |
| `channel_id` | str | `"0"` | 渠道ID |

#### `log_click(data_list, channel_id="0")`
上报点击数据。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `data_list` | str | 必填 | JSON格式点击数据 |
| `channel_id` | str | `"0"` | 渠道ID |

#### `log_stock_browse(stock_id)`
上报股票浏览记录。
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stock_id` | str | 是 | 股票代码 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "log_stock_browse" --kwargs '{"stock_id":"300827"}'
```

#### `log_browse_count(count=5)`
上报今日浏览次数。
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `count` | int | `5` | 浏览次数 |
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "log_browse_count"
```

#### `log_simulate_normal_usage()`
一键模拟正常用户使用行为（登录+浏览+点击+计数），防风控推荐使用。
```bash
python3 skills/kpl_api/scripts/call_kpl.py --method "log_simulate_normal_usage"
```

---

## 意图路由表

| 用户意图 | 首选方法 | 备选/补充方法 |
|---------|---------|-------------|
| 看龙虎榜/今日榜单 | `lhb_get_stock_list` | `lhb_top_title`（概览） |
| 某只股票龙虎榜明细 | `lhb_add` | — |
| 查大盘/指数行情 | `hq_index_info` | `zhishu_zs_trend`（走势图） |
| 查市场情绪/涨跌统计 | `hq_market_mood` | `hq_home_dingpan`（盯盘） |
| 查全球指数 | `hq_global_index` | — |
| 查人气股/热门股 | `hq_popular_stocks` | — |
| 查某股票盘口/买卖档 | `stock_pankou` | `stock_bid`（五档） |
| 查某股票实时行情 | `stock_realdata` | — |
| 查某股票分时走势 | `stock_trend` | `stock_dadan_trend`（大单分时） |
| 查某股票所属板块 | `stock_featured_section` | — |
| 查某股票消息/公告 | `stock_message_bar` | `user_stock_art_title` |
| 查K线（今日） | `kline_today` | — |
| 查K线（历史） | `kline_history` | `kline_interval`（区间统计） |
| 查大单K线 | `kline_dadan` | `kline_history_dadan`（历史大单） |
| 查涨停K线/复盘 | `kline_zhangting` | `kline_history_zhangting`（历史涨停） |
| 查概念/题材热点 | `conception_hotpoint` | `conception_zhibo`（实时异动） |
| 查板块详情/排名 | `plate_info_qj` | `plate_introduction`、`plate_son_info` |
| 查板块分时 | `conception_bk_fenshi` | `zhishu_trend` |
| 查指数盘口/成交量 | `zhishu_pankou` | `zhishu_vol` |
| 查资讯/新闻 | `article_index` → `article_sel_list` | `article_focus_msg`（详情） |
| 查专栏 | `article_column_list` → `article_column_info` | — |
| 查评论 | `comments_get` | — |
| 查用户权限/VIP等级 | `user_permission` | — |
| 刷新自选股 | `user_select_stock_refresh` | — |
| 防风控/模拟正常使用 | `log_simulate_normal_usage` | — |

## Safety Rules

- 仅允许调用 `KPLApi` 类中已定义的方法（共59个），拒绝执行任意 shell 文本。
- `TOKEN`、`USER_ID`、`DEVICE_ID` 为敏感凭证，不得在回复中明文展示。
- 未经用户明确要求，不得修改 `kpl_api.py` 中的认证参数。
- 返回内容超过 200 行时，只输出摘要与关键字段。

## Additional Notes

- 方法签名来源：`skills/kpl_api/scripts/kpl_api.py`
- 调用入口：`skills/kpl_api/scripts/call_kpl.py`
- 本地调用示例见 [examples.md](examples.md)
