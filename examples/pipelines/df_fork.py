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

from disdat.pipe import PipeTask
import disdat.api as api
from df_dup import DataMaker
import luigi
import pandas as pd

"""
Fork Pipe

Take an input DataFrame.  For each row, convert to a json string, and send to an upstream
task specified by the string fork_task_str ('module.Class').

Pre Execution:
$export PYTHONPATH=$DISDAT_HOME/disdat/examples/pipelines
$dsdt context examples; dsdt switch examples

Execution:
$python ./df_fork.py
or:
$dsdt apply - - df_fork.DFFork

"""


class DFFork(PipeTask):
    """ Given a dataframe, fork a task for each presentable

    Luigi Parameters:
        fork_task (str):  Disdat task 'module.Class' string.  This task should have two parameters: input_row (json string)
            and row_index (int).

    Returns:
        A list of produced HyperFrames

    """
    fork_task_str = luigi.Parameter(default=None)

    def pipe_requires(self, pipeline_input=None):
        """ For each row in the dataframe, create an upstream task with the row

        Args:
            pipeline_input: Input bundle data

        Returns:
            None
        """

        if not isinstance(pipeline_input, pd.DataFrame):
            print "DFFork expects DataFrame input bundle."
            return

        if pipeline_input is None:
            self.add_dependency('example_data', DataMaker, {})

        if self.fork_task_str is None:
            print "DFFork requires upstream tasks to fork to.  Specify '--fork_task_str <module.Class>'"
            return

        for i in range(0, len(pipeline_input.index)):
            json_row = pipeline_input[i:i + 1].to_json(orient='records')
            row_index = pipeline_input.index[i]
            self.add_dependency("output_{}".format(row_index),  self.fork_task_str,
                                {'input_row': json_row, 'input_idx': row_index})

        return

    def pipe_run(self, pipeline_input=None, **kwargs):
        """ Given a dataframe, split each row into the fork_task_str task class.

        Return a bundle of each tasks bundle.

        Args:
            pipeline_input: Input bundle data
            **kwargs: keyword args from input hyperframe and inputs to transform

        Returns:
            Array of Bundles (aka HyperFrames) from the forked tasks

        """

        # Note: There are two ways to propagate our outputs to our final output bundle


        data = []
        for k, v in kwargs.iteritems():
            if 'output_' in k:
                data.append(v)

        print "DFFork: Returning data {}".format(data)

        return data


if __name__ == "__main__":
    api.apply('examples', '-', '-', 'DFFork', params={'fork_task_str':'df_dup.DFDup'})
