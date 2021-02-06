/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 * @date: 2021-02-03
 */
import Article from '../models/article.model';
import { BaseContext } from 'koa';

export default class ArticleController {
    static async getArticleList(ctx: BaseContext) {
        const {
            current_page = 1,
            page_size = 8,
            keyword = '',
            tag = '',
            publish = 'ALL'
        } = ctx.query;
        
        try {
            const querys: {
                publish?: number,
                $or?: any,
                tag?: any
            } = {};
            
            const fields = {
                content: false,
                __v: false
            }

            if (publish === '0' || publish === '1') {
                querys.publish = Number(publish);
            }

            if (keyword !== '') {
                const keywordReg = new RegExp(keyword);
                querys.$or = [
                    { 'title': keywordReg },
                    { 'desc': keywordReg }
                ];
            }

            if (tag !== '') {
                querys.tag = {$in: [tag]};
            }

            const opts = {
                sort: { 'update_at': '-1' },
                skip: Number((current_page - 1) * page_size),
                limit: Number(page_size)
            };

            const result = await Article.find(querys, fields, opts).sort({
                'update_at': '-1'
            });

            const total = await Article.countDocuments(querys);

            ctx.body = {
                code: 1,
                msg: 'success',
                data: {
                    items: result || [],
                    total: Number(total),
                    current_page: Number(current_page),
                    page_size: Number(page_size)
                }
            }
        } catch (err) {
            console.log(err);
            ctx.body = {
                code: 0,
                msg: 'Internal Server Error'
            };
        }
    };

    static async postArticle(ctx: any) {
        try {
            const res = await new Article(ctx.request.body).save();
            if (res) {
                ctx.body = {
                    code: 1,
                    msg: 'post success'
                };
                return;
            }
        } catch (err) {
            console.log(err);
        }
        ctx.body = {
            code: 0,
            msg: 'failed, pleas check your form'
        }
    };
    
    static patch = async (ctx: BaseContext) => {};
    static delete = async (ctx: BaseContext) => {};
}
