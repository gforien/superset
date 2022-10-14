# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import logging
import os

from flask import Flask

from superset.initialization import SupersetAppInitializer

logger = logging.getLogger(__name__)

# Silence many info logs
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('alembic.runtime.migration').setLevel(logging.WARNING)

logger.warning("\n\n")
logger.setLevel(logging.ERROR)
logging.getLogger(__name__).setLevel(logging.WARNING)
logging.getLogger('superset').setLevel(logging.WARNING)
logging.getLogger('superset.stats_logger').setLevel(logging.WARNING)
logging.getLogger('superset.models').setLevel(logging.WARNING)
logging.getLogger('superset.utils.logging_configurator').setLevel(logging.WARNING)
logging.getLogger('superset.views.base').setLevel(logging.ERROR)

# Silence critical section logs
logging.getLogger('superset.sql_parse').setLevel(logging.WARNING)
logging.getLogger('superset.sql_lab').setLevel(logging.WARNING)
logging.getLogger('superset.sqllab.command').setLevel(logging.WARNING)

def create_app() -> Flask:
    app = SupersetApp(__name__)

    try:
        # Allow user to override our config completely
        config_module = os.environ.get("SUPERSET_CONFIG", "superset.config")
        app.config.from_object(config_module)

        app_initializer = app.config.get("APP_INITIALIZER", SupersetAppInitializer)(app)
        app_initializer.init_app()

        return app

    # Make sure that bootstrap errors ALWAYS get logged
    except Exception as ex:
        logger.exception("Failed to create app")
        raise ex


class SupersetApp(Flask):
    pass
