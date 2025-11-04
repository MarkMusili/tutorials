/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "../utils";


export class TodoList extends Component {
    static template = 'awesome_owl.TodoList'
    static components = { TodoItem };

    setup() {
        this.todos = useState([]);
        this.nextId = 1;
        this.inputRef = useAutofocus("input_value")
    }

    addTodo (ev) {
        if (ev.keyCode === 13 & ev.target.value != "" ) {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    toggleState (id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.isCompleted = !todo.isCompleted;
        };
    }
    removeTodo (id) {
        const todoIndex = this.todos.findIndex(t => t.id === id);
        if (todoIndex >= 0) {
            this.todos.splice(todoIndex, 1)
        };
    }
}