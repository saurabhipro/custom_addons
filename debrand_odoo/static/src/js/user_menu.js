/** @odoo-module **/


import { registry } from "@web/core/registry";
import { DebugMenu } from "@web/core/debug/debug_menu";

const { Component, useExternalListener } = owl;




registry.category("user_menuitems").remove('odoo_account');
registry.category("user_menuitems").remove('documentation');
registry.category("user_menuitems").remove('support');
registry.category("user_menuitems").remove('install_pwa');
registry.category("user_menuitems").remove('shortcuts');
registry.category("user_menuitems").remove("web_tour.tour_enabled")








