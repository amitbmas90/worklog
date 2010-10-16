import tornado.web
from utils.timesince import smartertimesince

class Footer(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/footer.html",
          calendar_link=self.request.path != '/'
         )
         
class Settings(tornado.web.UIModule):
    def render(self, settings):
        return self.render_string("modules/settings.html",
           settings_json=tornado.escape.json_encode(settings),
         )

class EventPreview(tornado.web.UIModule):
    def render(self, event):
        add_ago = smartertimesince(event.add_date)
        user_name = ''
        if event.user.first_name:
            user_name = event.user.first_name
        elif event.user.email:
            user_name = event.user.email
        return self.render_string("modules/eventpreview.html",
          event=event, add_ago=add_ago, user_name=user_name
         )
         
         