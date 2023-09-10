import TranslatePodcast from './views/TranslatePodcast.vue'
import MyPage from './views/MyPage.vue'
import TestCase from './components/TestCase.vue'
import {createRouter,createWebHashHistory} from 'vue-router';

const routes = [
    {path: '/', component: TranslatePodcast},
    {path: '/mypage', component: MyPage},
    {path: '/test', component: TestCase}
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router;