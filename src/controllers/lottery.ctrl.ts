import Koa from 'koa';
import axios, { AxiosResponse } from 'axios';

import { LotteryType } from './lottery.type';

export default class LotteryController {
    static async get(ctx: Koa.Context) {
        /**
         * get the lottery info from cwl.gov.cn api
         * @method get
         * @param {Koa.Context} ctx
         * @return
         */
        const typeName: LotteryType = ctx.query.type;
        const url = `http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=${typeName}&issueCount=1`;
        const res: AxiosResponse = await axios.get(url, {headers: {'referer': 'http://www.cwl.gov.cn/'}});
        ctx.response.body = res.data;
    }
}