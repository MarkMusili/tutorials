/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { Card } from "@awesome_owl/card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card };
    static props = {};

    setup() {
        this.plainTitle = "Hello <b>World</b>";
        this.plainContent = "This is <i>plain</i> content";

        this.htmlTitle = markup("Hello <b>World</b>");
        this.htmlContent = markup("This is <i>HTML</i> content");
    }
}
