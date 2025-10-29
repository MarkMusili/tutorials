/** @odoo-module **/
/** @odoo-module alias=@awesome_owl/playground **/
import { Component } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter };
    static props = {};
}
