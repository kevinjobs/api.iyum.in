import os
import unittest
import app
import manage
import flask_migrate

class TestApp(unittest.TestCase):

	def setUp(self):
		app_ctx = manage.app.app_context()
		app_ctx.push()
		flask_migrate.init()
		flask_migrate.migrate()
		flask_migrate.upgrade()
		app_ctx.pop()
		manage.app.config['TESTING'] = True
		self.client = manage.app.test_client()

	def tearDown(self):
		os.system('rm -rf ./migrations')
		os.system('rm -f ./example.db')
	
	def test_articles(self):
		# post '/api/v1/articles'
		req_route = '/api/v1/articles'
		req_json = {
			'cover': 'test_cover',
			'title': 'test_title',
			'author': 'test_author',
			'content': 'test_content',
			'tags': 'tag1,tag2',
			'category': 'test_cate'
		}
		resp_json = { 'code': 0, 'msg': 'ok', 'data': None}
		resp = self.client.post(req_route, json=req_json)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content_type, 'application/json')
		self.assertEqual(resp.get_json(), resp_json)

		# get '/api/v1/articles'
		req_route = '/api/v1/articles'
		resp_json = {
			'code': 0,
			'msg': 'ok',
			'data': {
				'items': [
					{
						'id': app.hash_ids.encode(1),
						'cover': 'test_cover',
						'title': 'test_title',
						'author': 'test_author',
						'content': 'test_content',
						'tags': 'tag1,tag2',
						'category': 'test_cate'
					}
				],
				'limit': 9,
				'page': 1,
				'total': 1
			}
		}
		resp = self.client.get(req_route, json=req_json)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content_type, 'application/json')
		self.assertEqual(resp.get_json(), resp_json)

		# get '/api/v1/article/<id>'
		req_route = '/api/v1/article/{0}'.format(app.hash_ids.encode(1))
		resp_json = {
			'code': 0,
			'msg': 'ok',
			'data': {
				'id': app.hash_ids.encode(1),
				'cover': 'test_cover',
				'title': 'test_title',
				'author': 'test_author',
				'content': 'test_content',
				'tags': 'tag1,tag2',
				'category': 'test_cate'
			}
		}
		resp = self.client.get(req_route)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content_type, 'application/json')
		self.assertEqual(resp.get_json(), resp_json)

		# put '/api/v1/article/<id>'
		req_route = '/api/v1/article/{0}'.format(app.hash_ids.encode(1))
		req_json = {
			'cover': 'test_cover',
			'title': 'test_title',
			'author': 'test_author',
			'content': 'test_content',
			'tags': 'tag1,tag2',
			'category': 'test_cate'
		}
		resp_json = {'code': 0, 'msg': 'ok', 'data': None}
		resp = self.client.put(req_route, json=req_json)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content_type, 'application/json')
		self.assertEqual(resp.get_json(), resp_json)

		# delete '/api/v1/article/<id>'
		req_route = '/api/v1/article/{0}'.format(app.hash_ids.encode(1))
		resp_json = {'code': 0, 'msg': 'ok', 'data': None}
		resp = self.client.delete(req_route)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content_type, 'application/json')
		self.assertEqual(resp.get_json(), resp_json)

		# post '/api/v1/user'
		req_route = '/api/v1/user'
		req_json = {
			'username': 'kevinjobs',
			'password': 'june1995'
		}
		resp_json = resp_json = {'code': 0, 'msg': 'ok', 'data': None}
		resp = self.client.post(req_route, json=req_json)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content_type, 'application/json')
		self.assertEqual(resp.get_json(), resp_json)

		# get '/api/v1/token'
		req_route = '/api/v1/token'
		req_json = ('kevinjobs','june1995')
		resp_json = resp_json = {'code': 0, 'msg': 'ok', 'data': None}
		resp = self.client.get(
			req_route,
			headers = {
				'Authorization': 'username="kevinjobs",password="june1995"'
			}
		)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.content_type, 'application/json')
		self.assertEqual(resp.get_json(), resp_json)


if __name__ == '__main__':
	unittest.main()