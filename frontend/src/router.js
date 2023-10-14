import TranslatePodcast from './views/TranslatePodcast.vue'
import MyPage from './views/MyPage.vue'
import SignUp from './views/SignUp.vue'
import LogIn from './views/LogIn.vue'
import {createRouter,createWebHashHistory} from 'vue-router';

const routes = [
    {path: '/', component: TranslatePodcast},
    {path: '/mypage', component: MyPage},
    {path: '/signup', component: SignUp},
    {path: '/login', component: LogIn}
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router;