import './App.css'
import { MainPage } from './pages/main-page.jsx'
import { Route,Routes } from 'react-router-dom'
import { AuthorizeForm } from './pages/auth/auth.jsx'
 import { useDispatch } from 'react-redux'
 import { useEffect } from 'react'
 import { setUser } from '../action/set-user.jsx'
 import { getUser } from '../api/get-user.jsx'
 import{ProtectedRoute}from '../components/protectedRoute.jsx'
import { FortsPage } from './pages/forts-page/fort-page.jsx'
import { ListTours } from './pages/list-tours/list-tours.jsx'

function App() {
  const dispatch=useDispatch()

  useEffect(()=>{
    const session = localStorage.getItem('session')
    if(session){
      getUser(session).then(userData=>{
        dispatch(setUser(userData))
      }).catch(() => {
        localStorage.removeItem('session')
        dispatch(setUser({}))
      })
    }
  },[dispatch])

 
 
  return (
    <div>
      <Routes>
      <Route path='/' element={
        <ProtectedRoute>
          <MainPage/>
        </ProtectedRoute>
      }/>
      <Route path='/auth' element={<AuthorizeForm/>}/>
      <Route path='/forts/:id' element={<FortsPage/>}/>
      <Route path='/list-tours' element={<ListTours/>}/>
      </Routes>
    </div>

  )
}

export default App