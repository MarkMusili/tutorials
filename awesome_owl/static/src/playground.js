/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "@awesome_owl/counter/counter";
import { Card } from "@awesome_owl/card/card";
import { TodoList } from "@awesome_owl/todo_list/todo_list";

export class Playground extends Component {
  static template = "awesome_owl.playground";

  static components = { Counter, Card, TodoList };
  static props = {};


  setup() {
    this.state = useState({ sum: 2 });
    this.plainTitle = "Hello <b>World</b>";
    this.plainContent = "This is <i>plain</i> content";

    this.htmlTitle = markup("Hello <b>World</b>");
    this.htmlContent = markup("This is <i>HTML</i> content");
  }

    incrementSum() {
        this.state.sum++;
    }
}
