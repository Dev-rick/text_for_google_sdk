import webapp2
import os
import jinja2
from datetime import datetime



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)






class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))
    def get_time(self):
        now = datetime.now()
        time = "%s:%s:%s / %s.%s.%s" % (now.hour + 2, now.minute, now.second, now.day, now.month, now.year)
        return time



class MainPage(BaseHandler):
    def get(self):
        now = super(MainPage, self).get_time()
        params = {"time": now}
        return self.render_template("lottery.html", params=params)  # render_template holt sich diese Datei



class LotteryHandler(BaseHandler):
    def get(self):
        now = super(LotteryHandler, self).get_time()
        import Lottery
        list_of_gen_numbers = Lottery.random_numbers(8)
        params = {"list_of_gen_numbers": list_of_gen_numbers, "time": now}
        return self.render_template("gen_numbers.html", params=params)






app = webapp2.WSGIApplication([
    ('/', MainPage),
    ("/lottery", LotteryHandler),
], debug=True)

