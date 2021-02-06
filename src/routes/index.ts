import Router from '@koa/router';
import koaBody from 'koa-body';
import LotteryController from '../controllers/lottery.ctrl';
import ArticleController from '../controllers/article.ctrl';

const router = new Router();

router.get('/lottery', LotteryController.get)

      .get('/article', ArticleController.getArticleList) // /article?type=[single | list]
      .post('/article', koaBody(), ArticleController.postArticle)
      .patch('/article')
      .delete('/article');

export default router;