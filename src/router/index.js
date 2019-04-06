import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import SearchSite from "@/components/SearchSite";
import UrteilView  from "@/components/UrteilView";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Search',
      component: SearchSite
    },
    {
      path: '/urteil/:az',
      name: 'Urteil',
      component: UrteilView,
      props: true,
      params: {
        "r": {},
        "search": {}
      }
    }
  ]
})
