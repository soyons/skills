"""
KPL (看盘龙) API 接口封装 - 量化交易版

保留量化交易相关接口：龙虎榜、行情、K线、盘口、板块、大单、资金流向等。
保留日志上报接口用于模拟正常用户行为，避免账号风控。
"""

import json
import time as _time
import requests


# ══════════════════════════════════════════════
# 从 HAR 文件提取的参数
# ══════════════════════════════════════════════

TOKEN = "f0ac84db0312669fa49c3837310deefa"
USER_ID = "3118201"
DEVICE_ID = "d5eb3c29566595bdece2a19a8ca2f0838f6337df"
USER_AGENT = "lhb/5.16.3 (com.kaipanla.www; build:2; iOS 18.0.1) Alamofire/4.9.1"


class KPLApi:
    """KPL API 客户端 - 量化交易版"""

    # 域名常量
    HOST_LHB = "https://applhb.longhuvip.com/w1/api/index.php"        # 龙虎榜
    HOST_HQ = "https://apphwshhq.longhuvip.com/w1/api/index.php"      # 行情数据
    HOST_HIS = "https://apphis.longhuvip.com/w1/api/index.php"         # 历史数据
    HOST_ARTICLE = "https://apparticle.longhuvip.com/w1/api/index.php"  # 资讯
    HOST_LOG = "https://applog.longhuvip.com/w1/api/index.php"         # 日志上报

    # 默认系统参数
    DEFAULT_VERSION = "5.16.0.3"
    DEFAULT_APIV = "w38"
    DEFAULT_PHONE_OS = "2"

    def __init__(self, token: str = TOKEN, user_id: str = USER_ID,
                 device_id: str = DEVICE_ID,
                 version: str = DEFAULT_VERSION):
        self.token = token
        self.user_id = user_id
        self.device_id = device_id
        self.version = version
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    # ──────────────────────────────────────────────
    # 内部方法
    # ──────────────────────────────────────────────

    def _sys_params(self, controller: str, action: str) -> dict:
        return {
            "PhoneOSNew": self.DEFAULT_PHONE_OS,
            "VerSion": self.version,
            "a": action,
            "apiv": self.DEFAULT_APIV,
            "c": controller,
        }

    def _auth_params(self, need_token=True, need_device=True) -> dict:
        params = {"UserID": self.user_id}
        if need_token:
            params["Token"] = self.token
        if need_device:
            params["DeviceID"] = self.device_id
        return params

    def _post(self, url: str, controller: str, action: str,
              business: dict = None, need_token=True, need_device=True) -> dict:
        data = self._sys_params(controller, action)
        data.update(self._auth_params(need_token, need_device))
        if business:
            data.update(business)
        resp = self.session.post(url, data=data, timeout=10)
        return resp.json()

    def _get(self, url: str, controller: str, action: str,
             business: dict = None, need_token=True, need_device=True) -> dict:
        params = self._sys_params(controller, action)
        params.update(self._auth_params(need_token, need_device))
        if business:
            params.update(business)
        resp = self.session.get(url, params=params, timeout=10)
        return resp.json()

    # ══════════════════════════════════════════════
    # 一、龙虎榜
    # ══════════════════════════════════════════════

    def lhb_update_list(self) -> dict:
        """获取龙虎榜更新列表（最新日期等元信息）"""
        return self._get(self.HOST_LHB, "LongHuBang", "UpdateList",
                         need_token=False, need_device=False)

    def lhb_get_stock_list(self, index: int = 0, st: int = 300) -> dict:
        """获取龙虎榜股票列表

        Args:
            index: 分页索引
            st: 数据条数
        """
        return self._post(self.HOST_LHB, "LongHuBang", "GetStockList",
                          {"Index": index, "st": st})

    def lhb_top_title(self) -> dict:
        """获取龙虎榜顶部标题（涨停/跌停/炸板统计）"""
        return self._post(self.HOST_LHB, "LongHuBang", "TopTitle",
                          need_device=False)

    def lhb_add(self, stock_id: str, date: str) -> dict:
        """查询个股龙虎榜明细

        Args:
            stock_id: 股票代码，如 "000815"
            date: 日期 YYYY-MM-DD
        """
        return self._post(self.HOST_LHB, "LongHuBang", "Add",
                          {"StockID": stock_id, "Time": date},
                          need_token=False, need_device=False)

    def lhb_dongcai_state(self) -> dict:
        """获取龙虎榜东财数据状态"""
        return self._post(self.HOST_LHB, "LongHuBangDongCai", "GetState",
                          need_token=False, need_device=False)

    # ══════════════════════════════════════════════
    # 二、主题/题材
    # ══════════════════════════════════════════════

    def theme_info(self, theme_id: str) -> dict:
        """获取主题详情

        Args:
            theme_id: 主题ID
        """
        return self._post(self.HOST_LHB, "Theme", "InfoGet",
                          {"ID": theme_id})

    def theme_plate_rank(self, zs_code: str) -> dict:
        """获取主题板块排名

        Args:
            zs_code: 指数代码，如 "801070"
        """
        return self._post(self.HOST_LHB, "Theme", "InfoBKR",
                          {"ZSCode": zs_code})

    # ══════════════════════════════════════════════
    # 三、排行榜
    # ══════════════════════════════════════════════

    def rank_ticai_stock_option(self) -> dict:
        """获取题材排行榜股票选项"""
        return self._get(self.HOST_LHB, "PaiHangBangOption",
                         "GetTiCaiStockOption", need_device=False)

    def rank_leading_times_option(self) -> dict:
        """获取领涨次数选项"""
        return self._post(self.HOST_LHB, "LeadingTimesOption",
                          "GetUserLeadingTimesOption", need_device=False)

    # ══════════════════════════════════════════════
    # 四、实时行情
    # ══════════════════════════════════════════════

    def hq_index_info(self, view: str = "1,2,3,4,5,6,7,8,9,10,11") -> dict:
        """获取大盘行情总览

        Args:
            view: 视图类型列表
        """
        return self._post(self.HOST_HQ, "Index", "GetInfo",
                          {"View": view}, need_device=False)

    def hq_home_dingpan(self) -> dict:
        """获取盯盘数据（涨停/跌停/炸板实时统计）"""
        return self._post(self.HOST_HQ, "HomeDingPan", "ModuleVersatile")

    def hq_market_mood(self) -> dict:
        """获取市场情绪指标"""
        return self._post(self.HOST_HQ, "MarketMood", "MoodNumCount",
                          need_token=False, need_device=False)

    def hq_global_index(self, view: str = "1,2,3,4,5,6") -> dict:
        """获取全球主要指数

        Args:
            view: 视图类型列表
        """
        return self._get(self.HOST_HQ, "GlobalIndex", "GlobalCommon",
                         {"View": view}, need_device=False)

    def hq_popular_stocks(self, index: int = 0, st: int = 6,
                          type_: int = 2, order: int = 1,
                          pid_type: int = 1) -> dict:
        """获取热门股票排行

        Args:
            index: 分页索引
            st: 每页条数
            type_: 数据类型
            order: 排序方式
            pid_type: 分类类型
        """
        return self._get(self.HOST_HQ, "GlobalIndex", "PopularStocks",
                         {"Index": index, "st": st, "type": type_,
                          "order": order, "pidType": pid_type},
                         need_device=False)

    def hq_xian_huo(self, time: str = "") -> dict:
        """获取现货数据

        Args:
            time: 时间戳
        """
        return self._post(self.HOST_HQ, "XianHuoData", "GetXianHuoList",
                          {"Time": time}, need_token=False, need_device=False)

    # ══════════════════════════════════════════════
    # 五、个股数据
    # ══════════════════════════════════════════════

    # ── 盘口/买卖盘 ──

    def stock_bid(self, stock_id: str) -> dict:
        """获取股票买卖盘（五档）

        Args:
            stock_id: 股票代码
        """
        return self._post(self.HOST_HQ, "StockL2Data", "GetStockBid",
                          {"StockID": stock_id}, need_device=False)

    def stock_pankou(self, stock_id: str, state: int = 1) -> dict:
        """获取股票盘口数据

        Args:
            stock_id: 股票代码
            state: 状态
        """
        return self._post(self.HOST_HQ, "StockL2Data", "GetStockPanKou_Narrow",
                          {"StockID": stock_id, "State": state})

    def stock_realdata(self, stock_id: str) -> dict:
        """获取股票实时数据（涨幅/量比/换手等）

        Args:
            stock_id: 股票代码
        """
        return self._post(self.HOST_HQ, "StockYiDongKanPan", "StockDPRealData",
                          {"StockID": stock_id}, need_device=False)

    # ── 分时走势 ──

    def stock_trend(self, stock_id: str) -> dict:
        """获取股票分时走势

        Args:
            stock_id: 股票代码
        """
        return self._post(self.HOST_HQ, "StockL2Data",
                          "GetStockTrendIncrementalPH",
                          {"StockID": stock_id},
                          need_token=False, need_device=False)

    def stock_dadan_trend(self, stock_id: str, time: str = "") -> dict:
        """获取股票大单分时走势

        Args:
            stock_id: 股票代码
            time: 增量起始时间
        """
        return self._post(self.HOST_HQ, "StockL2Data",
                          "GetStockDaDanTrendIncremental",
                          {"StockID": stock_id, "Time": time},
                          need_device=False)

    # ── 板块关联 ──

    def stock_featured_section(self, stock_id: str) -> dict:
        """获取个股所属板块

        Args:
            stock_id: 股票代码
        """
        return self._get(self.HOST_HQ, "StockL2Data", "GetFeaturedSection",
                         {"StockID": stock_id},
                         need_token=False, need_device=False)

    def stock_message_bar(self, stock_id: str) -> dict:
        """获取个股消息/公告

        Args:
            stock_id: 股票代码
        """
        return self._get(self.HOST_HQ, "StockMessageBar", "MessageBarInfo",
                         {"StockID": stock_id},
                         need_token=False, need_device=False)

    # ══════════════════════════════════════════════
    # 六、K线数据
    # ══════════════════════════════════════════════

    def kline_today(self, stock_id: str, type_: str = "d",
                    index: int = 0, st: int = 400) -> dict:
        """获取今日K线数据

        Args:
            stock_id: 股票代码
            type_: d=日线 w=周线 m=月线
            index: 起始索引
            st: 数据条数
        """
        return self._post(self.HOST_HQ, "StockLineData", "GetKLineToday_W14",
                          {"StockID": stock_id, "Type": type_,
                           "Index": index, "st": st},
                          need_device=False)

    def kline_zhangting(self, stock_id: str) -> dict:
        """获取K线涨停标记数据

        Args:
            stock_id: 股票代码
        """
        return self._post(self.HOST_HQ, "StockLineData", "GetKLineZhangTing",
                          {"StockID": stock_id},
                          need_token=False, need_device=False)

    def kline_dadan(self, stock_id: str, type_: str = "d") -> dict:
        """获取K线大单数据

        Args:
            stock_id: 股票代码
            type_: K线类型
        """
        return self._post(self.HOST_HQ, "StockLineData",
                          "GetKLineTodayDaDanNew",
                          {"StockID": stock_id, "Type": type_},
                          need_token=False, need_device=False)

    def kline_history(self, stock_id: str, type_: str = "d",
                      index: int = 0, st: int = 130,
                      is_fs: int = 1) -> dict:
        """获取历史K线数据

        Args:
            stock_id: 股票代码
            type_: d=日线 w=周线 m=月线
            index: 起始索引
            st: 数据条数
            is_fs: 是否复权
        """
        return self._post(self.HOST_HIS, "StockLineData", "GetKLineDay_W14",
                          {"StockID": stock_id, "Type": type_,
                           "Index": index, "st": st, "Is_FS": is_fs},
                          need_device=False)

    def kline_history_dadan(self, stock_id: str, type_: str = "d",
                            index: int = 0, st: int = 131) -> dict:
        """获取历史大单K线数据

        Args:
            stock_id: 股票代码
            type_: K线类型
            index: 起始索引
            st: 数据条数
        """
        return self._post(self.HOST_HIS, "StockLineData", "GetDaDanKLine2New",
                          {"StockID": stock_id, "Type": type_,
                           "Index": index, "st": st},
                          need_device=False)

    def kline_interval(self, stock_id: str, type_: str = "d",
                       index: int = 0, st: int = 47) -> dict:
        """获取K线区间统计数据

        Args:
            stock_id: 股票代码
            type_: K线类型
            index: 起始索引
            st: 数据条数
        """
        return self._post(self.HOST_HIS, "StockLineData", "GetLineInterval",
                          {"StockID": stock_id, "Type": type_,
                           "Index": index, "st": st},
                          need_device=False)

    def kline_history_zhangting(self, stock_id: str,
                                index: int = 0, st: int = 20) -> dict:
        """获取历史涨停复盘数据

        Args:
            stock_id: 股票代码
            index: 分页索引
            st: 每页条数
        """
        return self._get(self.HOST_HIS, "HisLimitResumption",
                         "GetDayZhangTing",
                         {"StockID": stock_id, "Index": index, "st": st},
                         need_token=False, need_device=False)

    # ══════════════════════════════════════════════
    # 七、概念/板块
    # ══════════════════════════════════════════════

    def conception_hotpoint(self) -> dict:
        """获取概念题材热点"""
        return self._post(self.HOST_HQ, "ConceptionPoint", "GetPoint",
                          need_token=False, need_device=False)

    def conception_zhibo(self) -> dict:
        """获取概念直播（实时异动）"""
        return self._post(self.HOST_HQ, "ConceptionPoint", "ZhiBoContent",
                          need_token=False, need_device=False)

    def conception_bk_fenshi(self, plate_id: str) -> dict:
        """获取板块分时走势

        Args:
            plate_id: 板块代码，如 "801070"
        """
        return self._get(self.HOST_HQ, "ConceptionPoint", "BKFenShiZhiBo",
                         {"PlateID": plate_id},
                         need_token=False, need_device=False)

    # ── 指数/板块数据 ──

    def zhishu_trend(self, stock_id: str, time: str = "") -> dict:
        """获取指数/板块分时走势

        Args:
            stock_id: 指数/板块代码
            time: 增量起始时间
        """
        return self._post(self.HOST_HQ, "ZhiShuL2Data",
                          "GetTrendIncremental",
                          {"StockID": stock_id, "Time": time},
                          need_token=False, need_device=False)

    def zhishu_pankou(self, stock_id: str) -> dict:
        """获取指数/板块盘口

        Args:
            stock_id: 指数/板块代码
        """
        return self._post(self.HOST_HQ, "ZhiShuL2Data", "GetPanKou",
                          {"StockID": stock_id, "Apiv": self.DEFAULT_APIV},
                          need_token=False)

    def zhishu_vol(self, stock_id: str, time: str = "") -> dict:
        """获取指数/板块成交量换手增量

        Args:
            stock_id: 指数/板块代码
            time: 增量起始时间
        """
        return self._post(self.HOST_HQ, "ZhiShuL2Data",
                          "GetVolTurIncremental",
                          {"StockID": stock_id, "Time": time},
                          need_token=False, need_device=False)

    def zhishu_parent_plate(self, stock_id: str) -> dict:
        """获取指数所属上级板块

        Args:
            stock_id: 指数/板块代码
        """
        return self._get(self.HOST_HQ, "ZhiShuL2Data", "GetParentPlateCode",
                         {"StockID": stock_id},
                         need_token=False, need_device=False)

    def zhishu_zs_trend(self, stock_id: str) -> dict:
        """获取大盘指数走势（上证/深成/创业）

        Args:
            stock_id: 指数代码，如 "SH000001"
        """
        return self._post(self.HOST_HQ, "StockL2Data", "GetZsTrend",
                          {"StockID": stock_id})

    # ── 板块排名 ──

    def plate_tc_config(self) -> dict:
        """获取板块题材分类配置"""
        return self._post(self.HOST_HQ, "ZhiShuRanking", "PlateTCConfig",
                          need_token=False, need_device=False)

    def plate_stock_tag(self, plate_id: str) -> dict:
        """获取板块成分股排行标签

        Args:
            plate_id: 板块代码
        """
        return self._get(self.HOST_HQ, "ZhiShuRanking", "GetGPCPHBTS_Tag",
                         {"PlateID": plate_id}, need_device=False)

    def plate_info_qj(self, plate_id: str,
                      r_start: str = "", r_end: str = "") -> dict:
        """获取板块区间涨跌信息

        Args:
            plate_id: 板块代码
            r_start: 区间开始日期
            r_end: 区间结束日期
        """
        return self._post(self.HOST_HQ, "ZhiShuRanking", "GetPlate_Info_QJ",
                          {"PlateID": plate_id,
                           "RStart": r_start, "REnd": r_end},
                          need_token=False, need_device=False)

    def plate_son_info(self, plate_id: str) -> dict:
        """获取子板块列表

        Args:
            plate_id: 板块代码
        """
        return self._get(self.HOST_HQ, "ZhiShuRanking", "SonPlate_Info",
                         {"PlateID": plate_id},
                         need_token=False, need_device=False)

    def plate_introduction(self, plate_id: str, stocks: str = "") -> dict:
        """获取板块简介及成分股列表

        Args:
            plate_id: 板块代码
            stocks: 成分股代码，逗号分隔
        """
        return self._get(self.HOST_HQ, "ZhiShuRanking",
                         "PlateIntroduction_Info",
                         {"PlateID": plate_id, "Stocks": stocks},
                         need_token=False, need_device=False)

    # ══════════════════════════════════════════════
    # 八、资讯
    # ══════════════════════════════════════════════

    def article_index(self, view: str = "1,2,3,4") -> dict:
        """获取资讯首页板块列表

        Args:
            view: 视图类型
        """
        return self._post(self.HOST_ARTICLE, "IndexPlate", "GetIndexList",
                          {"view": view}, need_device=False)

    def article_sel_list(self, index: int = 0, st: int = 20,
                         pre_index: int = 0,
                         select: str = "0,1,2") -> dict:
        """获取精选资讯列表

        Args:
            index: 分页索引
            st: 每页条数
            pre_index: 上一页索引
            select: 类型筛选
        """
        return self._post(self.HOST_ARTICLE, "ForumsMsgJX", "GetSelList",
                          {"Index": index, "st": st,
                           "PreIndex": pre_index, "Select": select})

    def article_column_list(self, index: int = 0, st: int = 10) -> dict:
        """获取专栏列表

        Args:
            index: 分页索引
            st: 每页条数
        """
        return self._post(self.HOST_ARTICLE, "ForumsMsgColumn", "GetList",
                          {"Index": index, "st": st})

    def article_column_info(self, column_id: str, index: int = 0,
                            st: int = 20, pre_index: int = 0,
                            select: str = "0,1,2") -> dict:
        """获取专栏详情

        Args:
            column_id: 专栏ID
            index: 分页索引
            st: 每页条数
            pre_index: 上一页索引
            select: 类型筛选
        """
        return self._post(self.HOST_ARTICLE, "ForumsMsgColumn", "GetInfo",
                          {"ColumnID": column_id, "Index": index,
                           "st": st, "PreIndex": pre_index,
                           "Select": select})

    def article_focus_msg(self, msg_id: str, type_: int = 0) -> dict:
        """获取关注消息详情

        Args:
            msg_id: 消息ID
            type_: 消息类型
        """
        return self._post(self.HOST_ARTICLE, "ForumsMsgJX", "GetFocusMsg",
                          {"MsgID": msg_id, "Type": type_})

    def article_theme_status(self, gid: str, g_type: int = 2) -> dict:
        """获取主题新闻状态

        Args:
            gid: 主题ID
            g_type: 主题类型
        """
        return self._post(self.HOST_ARTICLE, "ThemeNews", "GetThemeStaus",
                          {"GID": gid, "GType": g_type}, need_device=False)

    # ══════════════════════════════════════════════
    # 九、评论
    # ══════════════════════════════════════════════

    def comments_get(self, stock_id: str, type_: int = 4,
                     index: int = 0, st: int = 20,
                     tsort: int = 9, day: str = "") -> dict:
        """获取评论列表

        Args:
            stock_id: 股票/主题 ID
            type_: 评论类型
            index: 分页索引
            st: 每页条数
            tsort: 排序方式
            day: 日期过滤
        """
        return self._post(self.HOST_LHB, "Comments", "Get",
                          {"StockID": stock_id, "Type": type_,
                           "Index": index, "st": st,
                           "Tsort": tsort, "Day": day})

    # ══════════════════════════════════════════════
    # 十、用户（仅保留量化相关）
    # ══════════════════════════════════════════════

    def user_permission(self, type_: int = 33) -> dict:
        """获取用户权限（判断VIP等级，决定可用接口）

        Args:
            type_: 权限类型
        """
        return self._post(self.HOST_LHB, "UserInfo", "GetPermission",
                          {"Type": type_}, need_device=False)

    def user_weituo_notify(self, stock_id: str) -> dict:
        """获取委托通知

        Args:
            stock_id: 股票代码
        """
        return self._get(self.HOST_LHB, "UserWeiTuo", "GetNotify",
                         {"StockID": stock_id}, need_device=False)

    def user_select_stock_refresh(self, stock_id_list: str) -> dict:
        """刷新自选股行情

        Args:
            stock_id_list: 股票代码列表，如 "SH000001"
        """
        return self._post(self.HOST_HQ, "UserSelectStock", "RefreshStockList",
                          {"StockIDList": stock_id_list})

    def user_stock_art_title(self, stock_id: str, type_: int = 1) -> dict:
        """获取个股相关文章/公告标题

        Args:
            stock_id: 股票代码
            type_: 类型
        """
        return self._post(self.HOST_HQ, "Index", "GetArtTitle",
                          {"StockID": stock_id, "Type": type_})

    # ══════════════════════════════════════════════
    # 十一、日志上报（模拟正常用户行为，防风控）
    # ══════════════════════════════════════════════

    def log_user_login(self) -> dict:
        """上报用户登录"""
        return self._get(self.HOST_LOG, "DataStatistics", "UserLogin",
                         need_token=False)

    def log_page_view(self, data_list: str, channel_id: str = "0") -> dict:
        """上报页面浏览数据

        Args:
            data_list: JSON格式浏览数据
            channel_id: 渠道ID
        """
        return self._get(self.HOST_LOG, "DataBatchStatistics", "CalUserPage",
                         {"DataList": data_list, "ChannelID": channel_id,
                          "PhoneOS": "2", "Version": self.version},
                         need_token=False)

    def log_click(self, data_list: str, channel_id: str = "0") -> dict:
        """上报点击数据

        Args:
            data_list: JSON格式点击数据
            channel_id: 渠道ID
        """
        return self._get(self.HOST_LOG, "DataBatchStatistics", "CalUserClick",
                         {"DataList": data_list, "ChannelID": channel_id,
                          "PhoneOS": "2", "Version": self.version},
                         need_token=False)

    def log_stock_browse(self, stock_id: str) -> dict:
        """上报股票浏览记录

        Args:
            stock_id: 股票代码
        """
        return self._get(self.HOST_LHB, "UserStockLastBrowse",
                         "UpdateStockLastBrowse",
                         {"StockID": stock_id}, need_device=False)

    def log_browse_count(self, count: int = 5) -> dict:
        """上报今日浏览次数

        Args:
            count: 浏览次数
        """
        return self._post(self.HOST_LHB, "UserInfo", "ModTodayBrowseCount",
                          {"Count": count})

    def log_simulate_normal_usage(self) -> dict:
        """模拟一次正常用户使用行为（登录+浏览上报），防风控"""
        ts = str(int(_time.time()))
        self.log_user_login()
        page_data = json.dumps([
            {"S": "4", "P0": "2", "P1": "0", "U": self.user_id, "Ct": ts}
        ])
        self.log_page_view(page_data)
        click_data = json.dumps([
            {"P0": "217", "P1": "0", "U": self.user_id, "Ct": ts}
        ])
        self.log_click(click_data)
        self.log_browse_count()
        return {"status": "ok", "timestamp": ts}


# ══════════════════════════════════════════════
# 使用示例
# ══════════════════════════════════════════════

if __name__ == "__main__":
    # 直接使用，参数已从 HAR 文件提取
    api = KPLApi()

    # 模拟正常登录行为（防风控）
    api.log_simulate_normal_usage()

    # 获取龙虎榜
    print(api.lhb_get_stock_list())

    # 获取概念热点
    print(api.conception_hotpoint())

    # 获取个股盘口
    print(api.stock_pankou("300827"))

    # 获取K线
    print(api.kline_today("300827"))
