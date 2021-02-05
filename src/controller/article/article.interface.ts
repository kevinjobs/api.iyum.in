/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 * @date: 2021-01-31
 */
export interface ArticleListResInterface {
  code: number,
  message: string,
  data: {
    count: number,
    page: number,
    limit: number,
    items: ArticleInterface[]
  }
}

export interface ArticleResInterface {
  code: number,
  message: string,
  data: {
    item: ArticleInterface
  }
}

export interface ArticleInterface {
  id: string,
  create: string,
  update: string,
  cover?: string,
  title: string,
  author?: string,
  content?: string,
  tags?: string[] | string,
  category?: string
}

export interface RawArticleInterface {
  [key: string]: string | number,
  id: number,
  create_time: string,
  update_time: string,
  cover: string,
  title: string,
  author: string,
  content: string,
  tags: string,
  category: string
}