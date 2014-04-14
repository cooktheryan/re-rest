# Copyright (C) 2014 SEE AUTHORS FILE
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Views.
"""
import uuid

from flask import current_app, jsonify

from flask.views import MethodView

from rerest import mq


class V0DeploymentAPI(MethodView):

    methods = ['POST']

    def put(self, project):
        """
        Creates a new deployment.
        """
        try:
            request_id = str(uuid.uuid4())
            mq_data = current_app.config['MQ']
            jc = mq.JobCreator(
                server=mq_data['SERVER'],
                port=int(mq_data['PORT']),
                user=mq_data['USER'],
                password=mq_data['PASSWORD'],
                vhost=mq_data['VHOST'],
                logger=current_app.logger,
                request_id=request_id
            )
            current_app.logger.info('Creating job for project %s' % project)
            jc.create_job(project)
            confirmation_id = jc.get_confirmation()
            if confirmation_id is None:
                current_app.logger.debug(
                    'Confirmation for %s was none meaning the '
                    'project does not exist. Request id: %s' % (
                        project, request_id))
                return jsonify({'status': 'project not found'}), 404

            current_app.logger.debug(
                'Confirmation for %s is %s. Request id: %s' % (
                    project, confirmation_id, request_id))
            return jsonify({'status': 'created', 'id': confirmation_id}), 201
        except KeyError, kex:
            current_app.logger.error(
                'Error creating job for %s. Missing '
                'something in the MQ config section? %s: %s. '
                'Request id: %s' % (
                    project, type(kex).__name__, kex, request_id))
        except Exception, ex:
            # As there is a lot of other possible network related exceptions
            # this catch all seems to make sense.
            current_app.logger.error(
                'Error creating job for %s. %s: %s. '
                'Request id: %s' % (
                    project, type(ex).__name__, ex, request_id))
            return jsonify({'status': 'error'}), 500


def make_routes(app):
    """
    Makes and appends routes to app.
    """
    deployment_api_view = V0DeploymentAPI.as_view('deployment_api_view')
    app.add_url_rule('/api/v0/<project>/deployment/',
                     view_func=deployment_api_view, methods=['PUT', ])
    app.logger.info('Added v0 routes.')
