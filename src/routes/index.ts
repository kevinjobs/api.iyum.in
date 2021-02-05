import Router from '@koa/router';
import LotteryController from '../controllers/lottery.ctrl';

const router = new Router();

router.get('/lottery', LotteryController.get);

export default router;