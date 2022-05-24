import Vue from 'vue';
import Router from 'vue-router';
import Cluster from './components/Cluster.vue';
import RunsDashboard from './components/RunsDashboard';
// import Result from './components/Result';
import Sandbox from './components/Sandbox';
import ProcessResult from "./components/results/ProcessResult";
import PipeResult from "./components/results/PipeResult.vue";

Vue.use(Router);

export default new Router({
    //mode: 'history',
    base: import.meta.env.BASE_URL,
    routes: [
        {
            path: '/runs',
            name: 'Runs Dashboard',
            component: RunsDashboard,
        },
        {
            path: '/runs/:threadid',
            name: 'Cluster-ThreadId',
            component: Cluster,
            props: true,
        },
        {
            path: '/cluster',
            name: 'Runs Dashboard',
            component: RunsDashboard,
        },
        {
            path: '/cluster/:threadid',
            name: 'Cluster-ThreadId',
            component: Cluster,
            props: true,
        },
        {
            path: '/result/:thread_id',
            name: 'Result-ThreadId',
            component: ProcessResult,
            props: true,
        },
        {
            path: '/result/:thread_id/:pipe_id',
            name: 'Result-PipeId',
            component: PipeResult,
            props: true,
        },
        {
            path: '/sandbox',
            name: 'Sandbox',
            component: Sandbox
        }
    ],
});
