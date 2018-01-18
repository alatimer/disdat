#
# Copyright 2017 Human Longevity, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
SimpleTree

A simple tree of pipes:   Task C <- Task B <- Task A

author: Kenneth Yocum
"""

from disdat.pipe import PipeTask, PipesExternalBundle
import luigi
import logging
from tree_leaves import B

PIPE_PKG = 'pipe'

_logger = logging.getLogger(__name__)


class SimpleTree(PipeTask):
    """
    Create a simple binary tree of tasks.   First level is B, last level is C. 
    """
    uuid          = luigi.Parameter(default='None')

    def pipe_requires(self, pipeline_input=None):
        """

        Args:
            pipeline_input:

        Returns:

        """

        for i in range(2):
            self.add_dependency('B_{}'.format(i), B, {'task_label': str(i), 'uuid': '12340000'})
        return

    def pipe_run(self, pipeline_input=None, B_0=None, B_1=None):
        """

        Args:
            pipeline_input:
            B_0:
            B_1:

        Returns:

        """

        return