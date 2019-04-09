import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import SearchSite from "@/components/SearchSite"
import UrteilView from "@/components/UrteilView"
import SearchResults from "@/components/SearchResults";

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

    },
    {
      path: '/search/:norm/:searchTerm',
      name: 'SearchResult',
      component: SearchResults
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    let position = { x: 0, y: 0 }
    // Keep scroll position when using browser buttons
    if (savedPosition) {
      position = savedPosition
    }

    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve(position)
      }, 100)
    })
  }
})
