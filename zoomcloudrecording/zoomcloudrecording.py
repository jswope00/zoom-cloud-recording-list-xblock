import pkg_resources
import requests
import urllib
from datetime import datetime

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

from django.conf import settings
from django.template import Context, Template


class ZoomCloudRecordingXBlock(XBlock):
    """
    Shows a list of Zoom Cloud Recording Meetings
    """
    display_name = String(
        display_name="Zoom Cloud Recordings",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Zoom Cloud Recordings"
    )
    host_id = String(default=None, scope=Scope.content, help="Your host id")
    meeting_number = Integer(default=None, scope=Scope.content)
    from_date = String(default=None, scope=Scope.content)
    to_date = String(default=None, scope=Scope.content)
    page_size = Integer(default=30, 
                        scope=Scope.content, 
                        help="Number of recordings on one page")
    page_number = Integer(default=1, 
                          scope=Scope.content)

    def get_recording_list(self):
        url = 'https://api.zoom.us/v1/recording/list'
        data = {
            'api_key': settings.ZOOM_API_KEY,
            'api_secret': settings.ZOOM_API_SECRET,
            'host_id': self.host_id,
            'page_number': self.page_number
        }
        if self.meeting_number:
            data['meeting_number'] = self.meeting_number
        if self.from_date:
            data['from'] = self.from_date
        if self.to_date:
            data['to'] = self.to_date

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        r = requests.post(url, data=urllib.urlencode(data), headers=headers)

        return self.make_meeting_list(r.json())

    def student_view(self, context=None):
        context['meetings'] = self.get_recording_list()

        fragment = Fragment()
        fragment.add_content(
            render_template(
                'static/html/zoomcloudrecording.html',
                context
            )
        )
        fragment.add_css(load_resource("static/css/zoomcloudrecording.css"))
        #fragment.add_css_url("http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/css/jquery.dataTables.css")
        fragment.add_javascript_url("http://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.4/jquery.dataTables.min.js")
        js_str = load_resource("static/js/src/zoomcloudrecording.js").replace("{page_size}", str(self.page_size))
        fragment.add_javascript(js_str)
        fragment.initialize_js('ZoomCloudRecordingBlock')
        return fragment

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        context['host_id'] = self.host_id or ''
        context['meeting_number'] = self.meeting_number or ''
        context['from_date'] = self.from_date or ''
        context['to_date'] = self.to_date or ''
        context['page_size'] = self.page_size
        context['page_number'] = self.page_number

        fragment = Fragment()
        fragment.add_content(
            render_template(
                'static/html/zoomcloudrecording_edit.html',
                context
            )
        )

        fragment.add_javascript(load_resource("static/js/src/zoomcloudrecording_edit.js"))
        fragment.initialize_js('ZoomCloudRecordingEditBlock')
        return fragment

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        host_id = data.get('host_id')
        meeting_number = data.get('meeting_number')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        page_size = data.get('page_size')
        page_number = data.get('page_number')

        if host_id:
            self.host_id = host_id
            self.meeting_number = meeting_number
            self.from_date = from_date
            self.to_date = to_date
            self.page_size = page_size or 30
            self.page_number = page_number or 1

            return {'result': 'success'}

        return {'result': 'error', 'reason': 'No host id provided'}

    @staticmethod
    def make_meeting_list(json):
        meeting_list = []
        if 'error' not in json:
            for meeting in json['meetings']:
                _time = datetime.strptime(meeting['start_time'][:10], '%Y-%m-%d')
                start_date = datetime.strftime(_time, '%B %d, %Y')

                d = dict(topic=meeting['topic'], start_time=start_date, recordings=[])

                for recording in meeting['recording_files']:
		    if 'file_type' in recording and recording['file_type'] == 'MP4':
                        rec = dict(start=recording['recording_start'][:-4],
                                   end=recording['recording_end'][:-4],
                                   play_url=recording['play_url'])
                        d['recordings'].append(rec)

                meeting_list.append(d)

        return meeting_list

def load_resource(resource_path):
    """
    Gets the content of a resource
    """
    resource_content = pkg_resources.resource_string(__name__, resource_path)
    return unicode(resource_content)

def render_template(template_path, context={}):
    """
    Evaluate a template by resource path, applying the provided context
    """
    template_str = load_resource(template_path)
    template = Template(template_str)
    return template.render(Context(context))
