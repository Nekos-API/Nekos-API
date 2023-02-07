import dynamic from 'next/dynamic'

const IDE = dynamic(() => import('../components/graphiql'), {
  loading: () => 'Loading...',
  ssr: false
})

export default function GraphiQL() {
  return <IDE />
}