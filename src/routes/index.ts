import * as express from 'express';
import { Router } from 'express-serve-static-core';
import ArticleResource from '@/controller/article';
import { getImageList, getImage } from '@/controller/image';

const router: Router = express.Router();

const article = new ArticleResource();

// articles list
router.get('/articles', article.getList);
// article
router.get('/article', article.getById);
router.post('/article', article.post);
router.delete('/article', article.deleteById);
router.patch('/article', article.patchById);

// images list
router.get('/images', getImageList);
router.post('/images');
// imges
router.get('/image', getImage);
router.put('/image');

export default router;