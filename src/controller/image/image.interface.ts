/*!
 * @author: kevinjobs
 * @version: 0.0.1
 * @homepage: https://mint-forge.com
 * @date: 2021-01-31
 */
export interface IImageList {
  code: number,
  message: string,
  data: {
    limit: number,
    page: number,
    count: number,
    items: IImage[]
  }
}

export interface IImage {
  id: number,
  create: string,
  update: string,
  title: string,
  author?: string,
  source: string,
  desc?: string,
  //
  tags?: string[],
  category?: string,
  // exif info
  exif?: IExif
}


export interface IExif {
  manufacturer: string,
  systemVersion: string,
  cameraModel: string,
  cameraLens: string,
  // lens info
  exposureTime: string,
  iso: number,
  // width & height
  width: number,
  length: number,
  // gps
  gps?: {
    latitude: number,
    latitudeRef: string,
    longitude: number,
    longitudeRef: string,
    altitude: number,
    altitudeRef: string,
    formattedAddress: string[]
  }
}

export interface IRawImage {
  [key: string]: any,
  id: number,
  create: string,
  update: string,
  title: string,
  author: string,
  source: string,
  desc: string,
  //
  tags: string,
  category: string,
  // exif info
  manufacturer: string,
  system_version: string,
  camera_model: string,
  camera_lens: string,
  // lens info
  exposure_time: string,
  iso: number,
  // width & height
  width: number,
  length: number,
  latitude: number,
  latitude_ref: string,
  longitude: number,
  longitude_ref: string,
  altitude: number,
  altitude_ref: string,
  position: string
}