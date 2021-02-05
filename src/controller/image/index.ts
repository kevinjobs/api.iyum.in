/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 */
import * as express from 'express';
import {
  IImage,
  IImageList,
  IRawImage
} from './image.interface';
import { CODE, MESSAGE } from '@/common';
import { hashids } from '@/utils';
import db from '@/db';

export function getImageList (req: express.Request, res: express.Response) {
  /**
   * get the image list from db
   * @method getImageList
   * @param {express.Request} req
   * @param {express.Response} res
   * @return {void}
   */
  let { limit, page } = req.query as any;

  if (limit === undefined || limit === '') limit = 9;
  if (page === undefined || page === '') page = 1;

  const sql = `
    SELECT * FROM images
    LIMIT ${limit}
    OFFSET ${(page-1)*limit}
  `

  db.all(sql, (err, rows) => {
    if (err) {
      res.json({
        code: CODE.DB_ERROR,
        message: MESSAGE.DB_ERROR
      })
    } else {
      const items: IImage[] = [];
      rows.map((row: IRawImage, index: number) => {
        items.push(_parseImage(row));
      });
      res.json({
        code: CODE.OK,
        message: MESSAGE.OK,
        data: {
          limit: limit,
          page: page,
          count: rows.length,
          items: items
        }
      } as IImageList)
    }
  })
}

export function getImage (req: express.Request, res: express.Response) {
  /**
   * get the image by id from db
   * @method getImage
   * @param {express.Request} req
   * @param {express.Response} res
   * @return
   */
  const { id } = req.query as any;

  const sql = `SELECT * FROM images WHERE id=${hashids.decode(id)}`

  // console.log(sql);

  db.get(sql, (err, row) => {
    if (err) {
      res.json({
        code: CODE.DB_ERROR,
        message: MESSAGE.DB_ERROR
      });
    } else {
      res.json({
        code: CODE.OK,
        message: CODE.OK,
        data: _parseImage(row)
      });
    }
  })
}

function _parseImage(rawImage: IRawImage) :IImage {
  /**
   * convert data from db to IImage type
   * @method _parseImage
   * @param {IRawImage} rawImage
   * @return {IImage}
   */
  const result: IImage =  {
    id: hashids.encode(rawImage['id']),
    create: rawImage['create_time'],
    update: rawImage['update_time'],
    title: rawImage['title'],
    author: rawImage['author'],
    source: rawImage['source'],
    desc: rawImage['desc'],
    tags: rawImage['tags'].split(','),
    category: rawImage['category'],
    exif: {
      manufacturer: rawImage['manufacturer'],
      systemVersion: rawImage['system_version'],
      cameraModel: rawImage['cameral_model'],
      cameraLens: rawImage['cameral_lens'],
      exposureTime: rawImage['exposure_time'],
      iso: rawImage['iso'],
      width: rawImage['width'],
      length: rawImage['length'],
      gps: {
        latitude: rawImage['latitude'],
        latitudeRef: rawImage['latitude_ref'],
        longitude: rawImage['longitude'],
        longitudeRef: rawImage['longitude_ref'],
        altitude: rawImage['altitude'],
        altitudeRef: rawImage['altitude_ref'],
        formattedAddress: rawImage['position'].split('|')
      }
    }
  }
  return result;
}