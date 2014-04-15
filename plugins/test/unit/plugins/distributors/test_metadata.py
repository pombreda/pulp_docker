import shutil
import tempfile
import unittest

from mock import Mock

from pulp.common.compat import json
from pulp_docker.common.models import DockerImage
from pulp_docker.plugins.distributors import metadata


class TestImagesFileContext(unittest.TestCase):

    def setUp(self):
        self.working_directory = tempfile.mkdtemp()
        self.conduit = Mock()
        self.conduit.get_repo_scratchpad.return_value = {u'tags': {u'latest': u'image_id'}}
        self.context = metadata.ImagesFileContext(self.working_directory, self.conduit)
        self.context.metadata_file_handle = Mock()

    def tearDown(self):
        shutil.rmtree(self.working_directory)

    def test_add_unit_metadata(self):
        unit = DockerImage('foo_image', 'foo_parent', 2048)
        test_result = {'id': 'foo_image'}
        result_json = json.dumps(test_result)
        self.context.add_unit_metadata(unit)
        self.context.metadata_file_handle.write.assert_called_once_with(result_json)

    def test_add_unit_metadata_with_tag(self):
        unit = DockerImage('foo_image', 'foo_parent', 2048)
        test_result = {'id': 'foo_image', 'Tag': 'bar'}
        result_json = json.dumps(test_result)
        self.context.labels['foo_image'] = 'bar'
        self.context.add_unit_metadata(unit)
        self.context.metadata_file_handle.write.assert_called_once_with(result_json)