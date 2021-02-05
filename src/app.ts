import Koa from 'koa';
import router from './routes';

const app = new Koa();

app.use(router.routes());

app.listen(3000, () => {
    console.log('server starting at 3000!');
});