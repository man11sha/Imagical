import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/components/LandingPage'
import AboutPage from '@/components/AboutPage'
import GalleryPage from '@/components/GalleryPage'
import ImageDisplay from '@/components/ImageDisplay'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage
    },
    {
      path: '/gallery',
      name: 'Gallery',
      component: GalleryPage
    },
    {
      path: '/about',
      name: 'AboutPage',
      component: AboutPage
    },
    {
      path: '/imageDisplay',
      name: 'ImageDisplay',
      component: ImageDisplay
    }
  ]
})
