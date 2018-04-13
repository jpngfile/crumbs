// this should be refactored to split components up
import { h, app } from 'hyperapp'
// use dev tools early on when you dev, u dummy
import { withLogger } from '@hyperapp/logger'
import { location, Route } from '@hyperapp/router'

const $ = (slt) => document.querySelector(slt)

const state = {
  board: {
    team: 'hello',
    headers: {
      test: ['string', 'aaa']
    }
  },
  location: location.state
}

const actions = {
  // important! it's not async team =>..., it's team => async () =>
  getTeam: team => async (state, actions) => {
    const payload = await fetch(`http://localhost:5000/api/${team}`)
    const board = await payload.json()
    actions.setBoard(board)
  },
  setBoard: board => ({ board }),
  sendForm: e => async (state, actions) => {
    e.preventDefault()

    const formData = new FormData()
    const team = $('#team').value

    formData.append('team', team)
    formData.append('file', $('#file').files[0])

    const payload = await fetch(`http://localhost:5000/api/upload`, {
      method: 'POST',
      body: formData
    })
    const board = await payload.json()

    actions.setBoard(board)
  },
  location: location.actions
}

const Sticky = ({ content }) => (
  <li>{content}</li>
)

const Header = ({ header, stickies }) => (
  <div>
    <h3>{header}</h3>
    <ul>
      {stickies.map((sticky) => (
        <Sticky content={sticky} />
      ))}
    </ul>
  </div>
)

const Board = ({ team, headers }) => (
  <div>
    <h1>{team}</h1>
    <div>
      {Object.keys(headers).map((key) => (
        <Header header={key} stickies={headers[key]} />
      ))}
    </div>
  </div>
)

const App = (state, actions) => ({ location, match }) => {
  // if no check, it'll do render loop and spam requests
  if (state.board.team !== match.params.team) {
    // actions.getTeam(match.params.team)
  }

  return (
    <Board team={state.board.team} headers={state.board.headers} />
  )
}

const view = (state, actions) => (
  <div>
    <h1>Upload a scrum board picture!</h1>
    <form>
      <input type="file" name="file" id="file" accept="image/*" capture /><br />
      <input type="text" name="team" id="team" placeholder="Team name!" />
      <input type="submit" onclick={e => actions.sendForm(e)} value="Scrum!" />
    </form>

    <Route path="/board/:team" state={state} actions={actions} render={App(state, actions)} />
  </div>
)

const main = withLogger(app)(state, actions, view, document.body)
const unsubscribe = location.subscribe(main.location)
