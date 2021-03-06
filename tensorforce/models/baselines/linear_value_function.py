# Copyright 2017 reinforce.io. All Rights Reserved.
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
# ==============================================================================

"""
Linear value function for baseline prediction in TRPO.

N.b. as part of TRPO implementation from https://github.com/ilyasu123/trpo

This code is under MIT license, for more information see LICENSE-EXT.
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import numpy as np

from tensorforce.models.baselines.value_function import ValueFunction


class LinearValueFunction(ValueFunction):
    def __init__(self):
        self.coefficients = None

    def fit(self, paths):
        feature_matrix = np.concatenate([self.get_features(path) for path in paths])
        returns = np.concatenate([path["returns"] for path in paths])

        columns = feature_matrix.shape[1]
        lamb = 2

        self.coefficients = np.linalg.lstsq(feature_matrix.T.dot(feature_matrix)
                                            + lamb * np.identity(columns), feature_matrix.T.dot(returns))[0]

    def predict(self, path):
        """
        Predict path value based on linear coefficients.

        :param path:
        :return: Returns value estimate or 0 if coefficients have not been set
        """

        if self.coefficients is None:
            return np.zeros(len(path["rewards"]))
        else:
            return self.get_features(path).dot(self.coefficients)
