/** @odoo-module **/

import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";

const loadStatistics = {
    dependencies: ["rpc"],
    start(env, { rpc }) {
        const statistics = reactive({});

        async function loadData() {
            console.log("Fetching data...");
            const data = await rpc('/awesome_dashboard/statistics');
            Object.assign(statistics, data);
        }

        loadData();
        setInterval(loadData, 600000);

        return statistics;
    }
}

registry.category("services").add("loadStatistics", loadStatistics);