import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'

import App from '../App.vue'

describe('App', () => {
  it('renders the chat workspace layout', () => {
    const wrapper = mount(App)

    expect(wrapper.text()).toContain('新建对话')
    expect(wrapper.text()).toContain('Tender Workspace')
    expect(wrapper.text()).toContain('smartTenderSystem')
  })
})
