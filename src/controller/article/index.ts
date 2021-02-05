/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 */
import * as dayjs from 'dayjs';
import { Request, Response } from 'express-serve-static-core';
import {
  ArticleListResInterface,
  ArticleResInterface,
  ArticleInterface,
  RawArticleInterface
} from './article.interface';
import { CODE, MESSAGE, DATE_FORMAT } from '@/common';
import { hashids } from '@/utils';
import db from '@/db';
import { NextFunction } from 'express';

export default class ArticleListResource {
  /**
   * 
   * 
   * 
   */
  public getList = (req: Request, res: Response) => {
    /**
     * get the article list from db
     * @method getArticles
     * @param {Request} req
     * @param {Response} res
     * @return {void}
     */
    let { limit, page } = req.query as any;
  
    if (limit === undefined || limit === '') limit = 9;
    if (page === undefined || page === '') page = 1;
  
    const sql = `select * from articles limit ${limit} offset ${(page-1)*limit}`
  
    db.all(sql, (err, rows) => {
      if (err) {
        res.json({
          code: CODE.DB_ERROR,
          message: MESSAGE.DB_ERROR
        })
      } else {
        const items: ArticleInterface[] = [];
        rows.map((row, index) => {
          items.push(this.parseArticle(row))
        })
        res.json({
          code: 1,
          message: MESSAGE.OK,
          data: {
            limit: limit,
            page: page,
            count: rows.length,
            items: items
          }
        } as ArticleListResInterface);
      }
    })
  }
  
  public getById = (req: Request, res: Response) => {
    /**
     * get the article by id from db
     * @method getArticle
     * @for
     * @param req the request of express 
     * @param res the response of express
     * @return {void}
     */
    let { id } = req.query as any;

    const sql = `SELECT * FROM articles WHERE id=${hashids.decode(id)}`
  
    db.get(sql, (err, row) => {
      if (err) {
        res.json({
          code: CODE.DB_ERROR,
          message: MESSAGE.DB_ERROR
        });
      }
      else {
        res.json({
          code: CODE.OK,
          message: MESSAGE.OK,
          data: {
            item: this.parseArticle(row)
          }
        } as ArticleResInterface);
      }
    })
  }

  public post = (req: Request, res: Response, next: NextFunction) => {
    /**
     * post a new article
     * @method post
     * @param {Request} req
     * @param {Response} res
     * @return
     */
    const article: ArticleInterface = req.body;

    const sql = `INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`

    const data = [
      undefined,
      article.create || dayjs().format(DATE_FORMAT),
      article.update || dayjs().format(DATE_FORMAT),
      article.cover,
      article.title,
      article.author,
      article.content,
      article.tags,
      article.category
    ]

    db.run(sql, data, (err) => {
      if (err) {
        res.json({
          code: CODE.DB_ERROR,
          message: CODE.DB_ERROR
        })
      } else {
        res.json({
          code: CODE.OK,
          message: MESSAGE.OK
        })
      }
    })
  }

  public patchById = (req: Request, res: Response, next: NextFunction) => {
    /**
     * patch an article by id
     * @method post
     * @param {Request} req
     * @param {Response} res
     * @return
     */
    const article: ArticleInterface = req.body;

    let rows = ['update_time=$update', 'create_time=$create']

    if (article.create) rows.push('create=$create');
    if (article.update) rows.push('update=$update');
    if (article.cover) rows.push('cover=$cover');
    if (article.title) rows.push('title=$title');
    if (article.author) rows.push('author=$author');
    if (article.content) rows.push('content=$content');
    if (article.tags) rows.push('tags=$tags');
    if (article.category) rows.push('category=$category');

    const sql = `UPDATE articles SET ${rows.join(',')} WHERE id=${hashids.decode(req.query['id'])}`

    const data = {
      $create: article.create || dayjs().format(DATE_FORMAT),
      $update: article.update || dayjs().format(DATE_FORMAT),
      $cover: article.cover,
      $title: article.title,
      $author: article.author,
      $content: article.content,
      $tags: article.tags,
      $category: article.category
    }

    db.run(sql, data, (err) => {
      if (err) {
        console.log(err);
        res.json({
          code: CODE.DB_ERROR,
          message: CODE.DB_ERROR
        })
      } else {
        res.json({
          code: CODE.OK,
          message: MESSAGE.OK
        })
      }
    })
  }

  public deleteById = (req: Request, res: Response) => {
    /**
     * delete an article by id
     * @method getArticle
     * @for
     * @param req the request of express 
     * @param res the response of express
     * @return {void}
     */
    let { id } = req.query as any;

    const sql = `DELETE FROM articles WHERE id=${hashids.decode(id)}`
  
    db.run(sql, (err) => {
      if (err) {
        // console.log(err);
        res.json({
          code: CODE.DB_ERROR,
          message: MESSAGE.DB_ERROR
        });
      }
      else {
        res.json({
          code: CODE.OK,
          message: MESSAGE.OK
        })
      }
    })
  }
  
  private parseArticle (rawArticle: RawArticleInterface) :ArticleInterface {
    /**
     * parse the article from raw article object
     * @method _parseArticle
     * @param {RawArticleInterface} rawArticle article from the db
     * @return {ArticleInterface} article formatted
     */
    const result: ArticleInterface = {
      id: hashids.encode(rawArticle['id']),
      create: rawArticle['create_time'],
      update: rawArticle['update_time'],
      cover: rawArticle['cover'],
      title: rawArticle['title'],
      author: rawArticle['author'],
      content: rawArticle['content'],
      tags: rawArticle['tags'],
      category: rawArticle['category']
    }
    return result;
  }
}