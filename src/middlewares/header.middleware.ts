/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 * @date: 2021-01-31
 */
import { Request, Response, NextFunction } from 'express-serve-static-core';

export default function (req: Request, res: Response, next: NextFunction) {
  res.set({
    'content-type': 'text/json'
  })
  next();
}