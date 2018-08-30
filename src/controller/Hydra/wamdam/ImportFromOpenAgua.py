#!/usr/bin/env python
# -*- coding: utf-8 -*-
# (c) Copyright 2013, 2014,2015 University of Manchester
#
# ExportCSV is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ExportCSV is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ExportCSV.  If not, see <http://www.gnu.org/licenses/>
#


"""
    A Hydra plug-in for exporting a hydra network to CSV files.
"""

import os, sys, csv
import json
import time
import argparse as ap
import logging

import pytz
from numpy import array

from controller.wamdamAPI.ExportTemplate import ExportTemplate

# from hydra_client.plugin import JsonConnection
# from hydra_client.output import write_progress, \
#                                 write_output, \
#                                 validate_plugin_xml, \
#                                 create_xml_response
#
# from hydra_base.exceptions import HydraPluginError

__location__ = os.path.split(sys.argv[0])[0]



# Python utility libraries.

from controller.Hydra.HydraLib.HydraException import HydraPluginError
from controller.Hydra.HydraLib.PluginLib import JsonConnection, \
    create_xml_response, \
    write_progress, \
    write_output

# General library for working with JSON objects
import json
# Used for working with files.
import os, sys, datetime

import logging

log = logging.getLogger(__name__)



class ExportCSV(object):
    """
    """
    # Connect to the Hydra server on the local machine
    # More info: http://umwrg.github.io/HydraPlatform/tutorials/plug-in/tutorial_json.html#creating-a-client
    ur = "https://data.openagua.org"
    conn = JsonConnection(ur)
    login_response = conn.login('amabdallah@aggiemail.usu.edu', 'xxxxxx!')

    Network = None
    Scenario = None
    timezone = pytz.utc

    def __init__(self, url=None, session_id=None):

        self.errors = []
        self.warnings = []
        self.files    = []
        url = "https://data.openagua.org"
        self.connection = JsonConnection(url)
        login_response = self.connection.login('amabdallah@aggiemail.usu.edu', 'TestOpenAgua!')
        # if session_id is not None:
        #     log.info("Using existing session %s", session_id)
        #     self.connection.session_id=session_id
        # else:
        #     self.connection.login()

        all_attributes = self.call('get_all_attributes')
        self.attributes = {}
        if not all_attributes:
            raise HydraPluginError("An error has occurred. Please check that the "
                                   "network and all attributes are available.")

        for attr in all_attributes:
            self.attributes[attr.id] = attr.name

        self.num_steps = 7


    def call(self, func, args={}):
        return self.connection.call(func, args)


    def export(self, network_id, scenario_id, output_folder):

        """
            Export a network (and possibly a scenario) to a folder. If the
            scenario and output folders are not specified, all the scenarios
            will be exported and the output location will be the desktop.
        """
        #source_id / project_id / network_id / template_id
        # https: // www.openagua.org / network / 1 / 913 / 610 / 347 / summary
        network_id=149


        write_output("Retrieving Network")
        write_progress(2, self.num_steps)
        if network_id is not None:
            #The network ID can be specified to get the network...
            try:
                network_id = int(network_id)
                x = time.time()
                network = self.call('get_network', {'network_id':network_id})
                log.info("Network retrieved in %s", time.time()-x)
            except:
                raise HydraPluginError("Network %s not found."%network_id)
        else:
            raise HydraPluginError("A network ID must be specified!")

        if output_folder is None:
            log.info("No output folder specified. Defaulting to desktop.")
            output_folder = os.path.expanduser("~/Desktop")
        elif not os.path.exists(output_folder):
            raise HydraPluginError("Output folder %s does not exist"%output_folder)

        network_dir = os.path.join(output_folder, "network_%s"%(network.name).replace(" ", "_"))

        if not os.path.exists(network_dir):
            os.mkdir(network_dir)
        else:
            logging.info("%s already exists", network_dir)
            for export_num in range(100):
                new_network_dir = os.path.join(output_folder, "%s(%s)"%(network_dir,export_num))
                if not os.path.exists(new_network_dir):
                    logging.info("exporting to %s", new_network_dir)
                    os.mkdir(new_network_dir)
                    network_dir = new_network_dir
                    break

        network.network_dir = network_dir

        if network.scenarios is None:
            raise HydraPluginError("Network %s has no scenarios!"%(network))

        if scenario_id is not None:
            write_progress(3, self.num_steps)
            for scenario in network.scenarios:
                if int(scenario.id) == int(scenario_id):
                    log.info("Exporting Scenario %s"%(scenario.name))
                    self.export_network(network, scenario)
                    break
            else:
                raise HydraPluginError("No scenario with ID %s found"%(args.scenario))
        else:
            log.info("No Scenario specified, exporting them all!")
            for scenario in network.scenarios:
                log.info("Exporting Scenario %s"%(scenario.name))
                self.export_network(network, scenario)

        self.files.append(network_dir)


    def export_network(self, network, scenario):
        """
            Write the output files based on the given network and scenario.
        """

        write_output("Exporting network")
        log.info("\n************NETWORK****************")
        scenario.target_dir = os.path.join(network.network_dir, scenario.name.replace(' ', '_'))

        if not os.path.exists(scenario.target_dir):
            os.mkdir(scenario.target_dir)

        network_file = open(os.path.join(scenario.target_dir, "network.csv"), 'w')

        network_attributes = self.get_resource_attributes([network])

        network_attributes_string = ""
        if len(network_attributes) > 0:
            network_attributes_string = ',%s'%(','.join(network_attributes.values()))

        network_heading   = "ID, Name, Type, Nodes, Links, Groups, Rules%s, Description\n" % (network_attributes_string)
        metadata_heading   = "Name %s\n"%(network_attributes_string)

        network_attr_units = []
        for attr_id, attr_name in network_attributes.items():
            network_attr_units.append(self.get_attr_unit(scenario, attr_id, attr_name))


        network_units_heading  = "Units,,,,,,,,,,%s\n"%(','.join(network_attr_units))

        values = ["" for attr_id in network_attributes.keys()]
        metadata_placeholder = ["" for attr_id in network_attributes.keys()]

        if network.attributes is not None:
            for r_attr in network.attributes:
                attr_name = network_attributes[r_attr.attr_id]
                value, metadata = self.get_attr_value(scenario, r_attr, attr_name, network.name)
                idx = network_attributes.keys().index(r_attr.attr_id)
                values[idx] = value
                metadata_placeholder[idx] = metadata

        if network.types is not None and len(network.types) > 0:
            net_type = network.types[0]['name']
        else:
            net_type = ""

        #Leave the links, groups and rules blank for now, as there may not be
        #any links, groups or rules.
        network_data = {
            "id"          : network.id,
            "name"        : network.name,
            "type"        : net_type,
            "nodes"       : "",
            "links"       : "",
            "groups"      : "",
            "rules"       : "",
            "values"      : ",%s"%(",".join(values)) if len(values) > 0 else "",
            "description" : network.description,

        }

        write_progress(4, self.num_steps)
        node_map = dict()
        if network.nodes:
            node_map = self.export_nodes(scenario, network.nodes)
            network_data['nodes'] = "nodes.csv"
        else:
            log.warning("Network has no nodes!")

        write_progress(5, self.num_steps)
        link_map = dict()
        if network.links:
            link_map = self.export_links(scenario, network.links, node_map)
            network_data['links'] = "links.csv"
        else:
            log.warning("Network has no links!")

        write_progress(6, self.num_steps)
        group_map = dict()
        if network.resourcegroups:
            group_map = self.export_resourcegroups(scenario, network.resourcegroups, node_map, link_map)
            network_data['groups'] = "groups.csv"
        else:
            log.warning("Network has no resourcegroups.")

        write_progress(7, self.num_steps)
        rules = self.export_rules(scenario, node_map, link_map, group_map)
        if len(rules) > 0:
            network_data['rules'] = "rules.csv"

        network_entry = "%(id)s,%(name)s,%(type)s,%(nodes)s,%(links)s,%(groups)s,%(rules)s%(values)s,%(description)s\n"%network_data

        if scenario.get('start_time') is not None and \
            scenario.get('end_time') is not None and\
            scenario.get('time_step') is not None:
            network_heading   = "ID, Name, Type, Nodes, Links, Groups, Rules, starttime, endtime, timestep %s, Description\n" % (network_attributes_string)
            network_data['starttime'] = scenario.start_time
            network_data['endtime']   = scenario.end_time
            network_data['timestep'] = scenario.time_step
            network_entry = "%(id)s,%(name)s,%(type)s,%(nodes)s,%(links)s,%(groups)s,%(rules)s,%(starttime)s,%(endtime)s,%(timestep)s%(values)s,%(description)s\n"%network_data


        log.info("Exporting network metadata")
        if metadata_placeholder.count("") != len(metadata_placeholder):
            warnings = self.write_metadata(os.path.join(scenario.target_dir, 'network_metadata.csv'),
                                metadata_heading,
                                [(network.name, metadata_placeholder)])
            self.warnings.extend(warnings)

        network_file.write(network_heading)
        network_file.write(network_units_heading)
        network_file.write(network_entry)


        log.info("Network export complete")

        log.info("networks written to file: %s", network_file.name)
        network_file.close()


    def export_nodes(self, scenario, nodes):
        write_output("Exporting nodes.")
        log.info("\n************NODES****************")

        #return this so that the link export can easily access
        #the names of the links.
        id_name_map = dict()

        #For simplicity, export to a single node & link file.
        #We assume here that fewer files is simpler.
        node_file = open(os.path.join(scenario.target_dir, "nodes.csv"), 'w')

        node_attributes = self.get_resource_attributes(nodes)

        node_attributes_string = ""
        if len(node_attributes) > 0:
            node_attributes_string = ',%s'%(','.join(node_attributes.values()))

        node_heading       = "Name, x, y, Type%s, description\n"%(node_attributes_string)
        metadata_heading   = "Name %s\n"%(node_attributes_string)

        node_attr_units = []
        for attr_id, attr_name in node_attributes.items():
            node_attr_units.append(self.get_attr_unit(scenario, attr_id, attr_name))

        node_units_heading  = "Units,,,,%s\n"%(','.join(node_attr_units) if node_attr_units else ',')

        node_entries = []
        metadata_entries = []
        for node in nodes:

            id_name_map[node.id] = node.name

            values = ["" for attr_id in node_attributes.keys()]
            metadata_placeholder = ["" for attr_id in node_attributes.keys()]
            if node.attributes is not None:
                for r_attr in node.attributes:
                    attr_name = node_attributes[r_attr.attr_id]
                    value, metadata = self.get_attr_value(scenario, r_attr, attr_name, node.name)
                    idx = node_attributes.keys().index(r_attr.attr_id)
                    values[idx] = value
                    metadata_placeholder[idx] = metadata

            if node.types is not None and len(node.types) > 0:
                node_type = node.types[0]['name']
            else:
                node_type = ""

            node_entry = "%(name)s,%(x)s,%(y)s,%(type)s%(values)s,%(description)s\n"%{
                "name"        : node.name,
                "x"           : node.x,
                "y"           : node.y,
                "type"        : node_type,
                "values"      : ",%s"%(",".join(values)) if len(values) > 0 else "",
                "description" : node.description if node.description is not None else "",
            }
            node_entries.append(node_entry)
            if metadata_placeholder.count("") != len(metadata_placeholder):
                metadata_entries.append((node.name, metadata_placeholder))

        warnings = self.write_metadata(os.path.join(scenario.target_dir, 'nodes_metadata.csv'),
                            metadata_heading,
                            metadata_entries)
        self.warnings.extend(warnings)

        node_file.write(node_heading)
        node_file.write(node_units_heading)
        node_file.writelines(node_entries)


        log.info("Nodes written to file: %s", node_file.name)
        node_file.close()
        return id_name_map


    def export_links(self, scenario, links, node_map):
        write_output("Exporting links.")
        log.info("\n************LINKS****************")

        #return this so that the group export can easily access
        #the names of the links.
        id_name_map = dict()

        #For simplicity, export to a single link file.
        #We assume here that fewer files is simpler.
        link_file = open(os.path.join(scenario.target_dir, "links.csv"), 'w')

        link_attributes = self.get_resource_attributes(links)

        link_attributes_string = ""
        if len(link_attributes) > 0:
            link_attributes_string = ',%s'%(','.join(link_attributes.values()))

        link_heading   = "Name, from, to, Type%s, description\n" % (link_attributes_string)
        metadata_heading   = "Name %s\n"%(link_attributes_string)


        link_attr_units = []
        for attr_id, attr_name in link_attributes.items():
            link_attr_units.append(self.get_attr_unit(scenario, attr_id, attr_name))

        link_units_heading  = "Units,,,,%s\n"%(','.join(link_attr_units) if link_attr_units else ',')

        link_entries = []
        metadata_entries = []
        for link in links:

            id_name_map[link.id] = link.name

            values = ["" for attr_id in link_attributes]
            metadata_placeholder = ["" for attr_id in link_attributes]
            if link.attributes is not None:
                for r_attr in link.attributes:
                    attr_name = link_attributes[r_attr.attr_id]
                    value, metadata = self.get_attr_value(scenario, r_attr, attr_name, link.name)
                    values[link_attributes.keys().index(r_attr.attr_id)] = value
                    metadata_placeholder[link_attributes.keys().index(r_attr.attr_id)] = metadata

            if link.types is not None and len(link.types) > 0:
                link_type = link.types[0]['name']
            else:
                link_type = ""

            link_entry = "%(name)s,%(from)s,%(to)s,%(type)s%(values)s,%(description)s\n"%{
                "name"        : link.name,
                "from"        : node_map[link.node_1_id],
                "to"          : node_map[link.node_2_id],
                "type"        : link_type,
                "values"      : ",%s"%(",".join(values)) if len(values) > 0 else "",
                "description" : link.description if link.description is not None else "",
            }
            link_entries.append(link_entry)

            if metadata_placeholder.count("") != len(metadata_placeholder):
                metadata_entries.append((link.name, metadata_placeholder))

        warnings = self.write_metadata(os.path.join(scenario.target_dir, 'links_metadata.csv'),
                            metadata_heading,
                            metadata_entries)
        self.warnings.extend(warnings)

        link_file.write(link_heading)
        link_file.write(link_units_heading)
        link_file.writelines(link_entries)
        log.info("Links written to file: %s", link_file.name)
        link_file.close()
        return id_name_map


    def export_resourcegroups(self, scenario, resourcegroups, node_map, link_map):
        """
            Export resource groups into two files.
            1:groups.csv defining the group name, description and any attributes.
            2:group_members.csv defining the contents of each group for this scenario
        """
        log.info("\n************RESOURCE GROUPS****************")
        write_output("Exporting groups.")

        group_file = open(os.path.join(scenario.target_dir, "groups.csv"), 'w')
        group_attributes = self.get_resource_attributes(resourcegroups)

        group_attributes_string = ""
        if len(group_attributes) > 0:
            group_attributes_string = ',%s'%(','.join(group_attributes.values()))

        group_attr_units = []
        for attr_id, attr_name in group_attributes.items():
            group_attr_units.append(self.get_attr_unit(scenario, attr_id, attr_name))

        group_heading   = "Name, Type, Members %s, description\n" % (group_attributes_string)
        group_units_heading  = "Units,,,%s\n"%(','.join(group_attr_units) if group_attr_units else ',')
        metadata_heading   = "Name %s\n"%(group_attributes_string)

        group_entries = []
        metadata_entries = []
        id_name_map = dict()
        for group in resourcegroups:
            id_name_map[group.id] = group.name

            values = ["" for attr_id in group_attributes.keys()]
            metadata_placeholder = ["" for attr_id in group_attributes.keys()]
            if group.attributes is not None:
                for r_attr in group.attributes:
                    attr_name = group_attributes[r_attr.attr_id]
                    value, metadata = self.get_attr_value(scenario, r_attr, attr_name, group.name)
                    values[group_attributes.keys().index(r_attr.attr_id)] = value
                    metadata_placeholder[group_attributes.keys().index(r_attr.attr_id)] = metadata

            if group.types is not None and len(group.types) > 0:
                group_type = group.types[0]['name']
            else:
                group_type = ""

            group_entry = "%(name)s,%(type)s,%(members)s,%(values)s,%(description)s\n"%{
                "name"        : group.name,
                "type"        : group_type,
                "members"     : "group_members.csv",
                "values"      : "%s"%(",".join(values)) if len(values) > 0 else "",
                "description" : group.description,
            }
            group_entries.append(group_entry)
            if metadata_placeholder.count("") != len(metadata_placeholder):
                metadata_entries.append((group.name, metadata_placeholder))

        warnings = self.write_metadata(os.path.join(scenario.target_dir, 'groups_metadata.csv'),
                            metadata_heading,
                            metadata_entries)

        self.warnings.extend(warnings)

        group_file.write(group_heading)
        group_file.write(group_units_heading)
        group_file.writelines(group_entries)
        log.info("groups written to file: %s", group_file.name)
        group_file.close()

        self.export_resourcegroupitems(scenario, id_name_map, node_map, link_map)

        return id_name_map


    def export_rules(self, scenario, node_map, link_map, group_map):
        """
            Export rules, which are chunks of text associated with resources and a scenario.
            :param scenario object to retrive the ID
            :param node map to get the name of a node from its id
            :param link map to get the name of a link from its id
            :param group map to get the name of a group from its id.
        """

        write_output("Exporting rules.")
        log.info("\n************RULES****************")

        rules = self.call('get_rules', {'scenario_id':scenario.id})

        if rules in (None, '') or len(rules) == 0:
            return []

        rule_entries = []
        #For simplicity, export to a single node & link file.
        #We assume here that fewer files is simpler.
        rule_file = open(os.path.join(scenario.target_dir, "rules.csv"), 'w')

        rule_heading       = "Name, Type, Resource, Text, Description\n"

        for rule in rules:
            if rule.ref_key == 'NODE':
                resource = node_map[rule.ref_id]
            elif rule.ref_key == 'LINK':
                resource = link_map[rule.ref_id]
            elif rule.ref_key == 'GROUP':
                resource = group_map[rule.ref_id]

            rule_entry = "%(name)s, %(type)s, %(resource)s, %(text)s, %(description)s\n"%{
                    "name"        : rule.name,
                    "type"        : rule.ref_key,
                    "resource"    : resource,
                    "text"        : rule.text,
                    "description" : rule.description,
            }

            rule_entries.append(rule_entry)

        rule_file.write(rule_heading)
        rule_file.writelines(rule_entries)

        log.info("Rules written to file: %s", rule_file.name)
        rule_file.close()

        return rule_entries


    def write_metadata(self, target_file, header, data):

        warnings = []
        if len(data) == 0:
            return warnings

        metadata_entries = []
        for m in data:
            try:
                metadata = m[1]
                metadata_vals = []
                for metadata_dict in metadata:
                    if metadata_dict == '':
                        metadata_vals.append("")
                    else:
                        metadata_text = []
                        for k, v in metadata_dict.items():
                            metadata_text.append("(%s;%s)"%(k,v))
                        metadata_vals.append("".join(metadata_text))
                metadata_entry = "%(name)s,%(metadata)s\n"%{
                    "name"        : m[0],
                    "metadata"    : "%s"%(",".join(metadata_vals)),
                }
                metadata_entries.append(metadata_entry)

            except Exception, e:
                log.exception(e)
                warnings.append("Unable to export metadata %s"%m)

        if len(metadata_entries) > 0:
            metadata_file = open(target_file, 'w')
            metadata_file.write(header)
            metadata_file.writelines(metadata_entries)
            metadata_file.close()

        return warnings


    def export_resourcegroupitems(self, scenario, group_map, node_map, link_map):
        """
            Export the members of a group in a given scenario.
        """
        group_member_file = open(os.path.join(scenario.target_dir, "group_members.csv"), 'w')

        group_member_heading   = "Name, Type, Member\n"
        group_member_entries   = []
        for group_member in scenario.resourcegroupitems:
            group_name = group_map[group_member.group_id]
            member_type = group_member.ref_key
            if member_type == 'LINK':
                member_name = link_map[group_member.ref_id]
            elif member_type == 'NODE':
                member_name = node_map[group_member.ref_id]
            elif member_type == 'GROUP':
                member_name = group_map[group_member.ref_id]
            else:
                raise HydraPluginError('Unrecognised group member type: %s'%(member_type))

            group_member_str = "%(group)s, %(type)s, %(member_name)s\n" % {
                'group': group_name,
                'type' : member_type,
                'member_name' : member_name,
            }
            group_member_entries.append(group_member_str)

        group_member_file.write(group_member_heading)
        group_member_file.writelines(group_member_entries)
        group_member_file.close()


    def get_resource_attributes(self, resources):
        #get every attribute across every resource
        attributes = {}
        for resource in resources:
            if resource.attributes is not None:
                for r_attr in resource.attributes:
                    if r_attr.attr_id not in attributes.keys():
                        attr_name = self.attributes[r_attr.attr_id]
                        attributes[r_attr.attr_id] = attr_name
        return attributes


    def get_attr_unit(self, scenario, attr_id, attr_name=None):
        """
            Returns the unit of a given resource attribute within a scenario
        """

        for rs in scenario.resourcescenarios:
            if rs.attr_id == attr_id:
                if rs.value.unit is not None:
                    return rs.value.unit

        log.warning("Unit not found in scenario '%s' for attr: %s", scenario.name, attr_name)

        return ''


    def get_attr_value(self, scenario, resource_attr, attr_name, resource_name):
        """
            Returns the value of a given resource attribute within a scenario
        """

        r_attr_id = resource_attr.id
        metadata = ()

        #if resource_attr.attr_is_var == 'Y':
        #    return 'NULL', ''

        for rs in scenario.resourcescenarios:
            if rs.resource_attr_id == r_attr_id:
                if rs.value.type == 'descriptor':
                    value = str(rs.value.value)
                elif rs.value.type == 'array':
                    value = rs.value.value
                    file_name = "array_%s_%s.csv"%(resource_attr.ref_key, attr_name)
                    file_loc = os.path.join(scenario.target_dir, file_name)
                    if os.path.exists(file_loc):
                        arr_file      = open(file_loc, 'a')
                    else:
                        arr_file      = open(file_loc, 'w')

                        if rs.value.metadata is not None:
                            for k, v in json.loads(rs.value.metadata).items():
                                if k == 'data_struct':
                                    arr_desc = ",".join(v.split('|'))
                                    arr_file.write("array , ,%s\n"%arr_desc)

                    arr_val = json.loads(value)

                    np_val = array(eval(repr(arr_val)))
                    shape = np_val.shape
                    n = 1
                    shape_str = []
                    for x in shape:
                        n = n * x
                        shape_str.append(str(x))
                    one_dimensional_val = np_val.reshape(1, n)
                    arr_file.write("%s,%s,%s\n"%
                                (
                                    resource_name,
                                    ' '.join(shape_str),
                                    ','.join([str(x) for x in one_dimensional_val.tolist()[0]]))
                                 )

                    arr_file.close()
                    value = file_name
                elif rs.value.type == 'scalar':

                    value = json.loads(rs.value.value)

                elif rs.value.type == 'timeseries':
                    value = json.loads(rs.value.value)

                    if value is None or value == {}:
                        log.debug("Not exporting %s from resource %s as it is empty", attr_name, resource_name)
                        continue

                    col_names = value.keys()
                    file_name = "timeseries_%s_%s.csv"%(resource_attr.ref_key, attr_name)
                    file_loc = os.path.join(scenario.target_dir, file_name)
                    if os.path.exists(file_loc):
                        ts_file      = open(file_loc, 'a')
                    else:
                        ts_file      = open(file_loc, 'w')

                        ts_file.write(",,,%s\n"%','.join(col_names))
                    if not value:
                        log.critical(attr_name)
                        log.critical(resource_name)
                        log.critical(resource_attr)
                        log.critical(value)
                    timestamps = value[col_names[0]].keys()
                    ts_dict = {}
                    for t in timestamps:
                        ts_dict[t] = []

                    for col, ts in value.items():
                        for timestep, val in ts.items():
                            ts_dict[timestep].append(val)

                    for timestep, val in ts_dict.items():
                            np_val = array(val)
                            shape = np_val.shape
                            n = 1
                            shape_str = []
                            for x in shape:
                                n = n * x
                                shape_str.append(str(x))
                            one_dimensional_val = np_val.reshape(1, n)
                            ts_file.write("%s,%s,%s,%s\n"%
                                        ( resource_name,
                                        timestep,
                                        ' '.join(shape_str),
                                        ','.join([str(x) for x in one_dimensional_val.tolist()[0]])))

                    ts_file.close()

                    value = file_name

                metadata = json.loads(rs.value.metadata)

                return (str(value), metadata)

        return ('', '')


def commandline_parser():
    parser = ap.ArgumentParser(
        description="""Export a network in Hydra to a set of CSV files.

Written by Stephen Knox <s.knox@ucl.ac.uk>
(c) Copyright 2013, University College London.
(c) Copyright 2014, University of Manchester.
        """, epilog="For more information visit www.hydraplatform.org",
        formatter_class=ap.RawDescriptionHelpFormatter)
    parser.add_argument('-t', '--network-id',
                        help='''Specify the network_id of the network to be exported.
                        If the network_id is not known, specify the network name. In
                        this case, a project ID must also be provided''')
    parser.add_argument('-s', '--scenario-id',
                        help='''Specify the ID of the scenario to be exported. If no
                        scenario is specified, all scenarios in the network will be
                        exported.
                        ''')
    parser.add_argument('-o', '--output-folder',
                        help='''Specify the ID of the scenario to be exported. If no
                        scenario is specified, all scenarios in the network will be
                        exported.
                        ''')
    parser.add_argument('-z', '--timezone',
                        help='''Specify a timezone as a string following the
                        Area/Location pattern (e.g. Europe/London). This
                        timezone will be used for all timeseries data that is
                        imported. If you don't specify a timezone, it defaults
                        to UTC.''')
    parser.add_argument('-u', '--server-url',
                        help='''Specify the URL of the server to which this
                        plug-in connects.''')
    parser.add_argument('-c', '--session_id',
                        help='''Session ID. If this does not exist, a login will be
                        attempted based on details in config.''')
    return parser

# NetworkName='Monterrey'



if __name__ == '__main__':
    parser = commandline_parser()
    args = parser.parse_args()
    exportCSV = ExportCSV(url=args.server_url, session_id=args.session_id)
    try:
        write_progress(1, exportCSV.num_steps)
        # validate_plugin_xml(os.path.join(__location__, 'plugin.xml'))


        if args.timezone is not None:
            exportCSV.timezone = pytz.timezone(args.timezone)

        exportCSV.export(args.network_id, args.scenario_id, args.output_folder)
        message = "Export complete"
    except HydraPluginError as e:
        message="An error has occurred"
        errors = [e.message]
        log.exception(e)
    except Exception, e:
        message="An error has occurred"
        log.exception(e)
        errors = [e]

    xml_response = create_xml_response('ExportCSV',
                                       args.network_id,
                                       [],
                                       exportCSV.errors,
                                       exportCSV.warnings,
                                       message,
                                       exportCSV.files)

    for main_dir in exportCSV.files:
        n = 0
        for x in os.walk(main_dir):
            if n == 0:
                for sub_dir in x[1]:
                    file_dir = '{}/{}'.format(main_dir, sub_dir)
                    exportTemplate = ExportTemplate('{}/{}.xlsx'.format(file_dir, sub_dir.replace(' ', '_')))

                    nodes_data_result = []
                    full_path = "{}/{}".format(file_dir, "nodes.csv")
                    if os.path.exists(full_path):
                        f = open(full_path)
                        csv_items = csv.DictReader(f)
                        for i, row in enumerate(csv_items):
                            row_data = ['', '', '', '', '', '', '', '', '', '']
                            row_data.insert(0, row[" Type"])
                            row_data.insert(1, row["Name"])
                            row_data.insert(7, row[" x"])
                            row_data.insert(8, row[" y"])
                            nodes_data_result.append(row_data)
                        exportTemplate.exportNodes(nodes_data_result)

                    links_data_result = []
                    full_path = "{}/{}".format(file_dir, "links.csv")
                    if os.path.exists(full_path):
                        f = open(full_path)
                        csv_items = csv.DictReader(f)
                        for i, row in enumerate(csv_items):
                            row_data = ['', '', '', '', '', '', '', '', '', '']
                            row_data.insert(0, row[" Type"])
                            row_data.insert(1, row["Name"])
                            row_data.insert(6, row[" from"])
                            row_data.insert(7, row[" to"])
                            links_data_result.append(row_data)
                        exportTemplate.exportLinkes(links_data_result)

                n += 1


    print xml_response