import Koa from 'koa';
import logger from 'koa-logger';
import router from './routes';
import * as mongodb from './db';

mongodb.connect();

const app = new Koa();

app.use(logger());

app.use(router.routes());

app.listen(3000, () => {
    console.log('server starting at 3000!');
});