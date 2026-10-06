import React from 'react'

const Chip = ({ status, text }) => {
  const statusClass = status.toLowerCase();
  return (
    <div className="v-chip">
      <div className={`chip-dot ${statusClass}`}></div>
      {text}
    </div>
  )
}

const TimelineBar = ({ startPercent, widthPercent, active }) => {
  return (
    <div className="timeline-container">
      <div 
        className={`timeline-bar ${active ? 'active' : ''}`} 
        style={{ left: `${startPercent}%`, width: `${widthPercent}%` }}
      ></div>
    </div>
  )
}

const App = () => {
  return (
    <div>
      {/* Header */}
      <header className="app-header">
        <div className="logo-area">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="24" height="24" fill="white"/>
            <circle cx="12" cy="12" r="6" fill="black"/>
          </svg>
          Nexus
        </div>
        <nav className="nav-links">
          <a href="#">Product</a>
          <a href="#">Solutions</a>
          <a href="#">Docs</a>
          <a href="#">Pricing</a>
        </nav>
        <button className="btn-square">
          Book a demo
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </button>
      </header>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-scrim"></div>
        <div className="hero-content">
          <h1 className="headline-fluid">Uncover complex system failures with brutal precision.</h1>
          <p className="hero-subtext">Deep-dive into event streams, analyze regression tests, and pinpoint errors across your entire infrastructure before they affect production.</p>
          <button className="btn-square btn-large">
            Start debugging
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </button>
        </div>
      </section>

      {/* Metrics Grid */}
      <section className="metrics-grid">
        <div className="metrics-cell">
          <div className="metric-value">4.2 <span className="metric-unit">M</span></div>
          <div className="metric-label">Traces Analyzed</div>
        </div>
        <div className="metrics-cell">
          <div className="metric-value">99.9 <span className="metric-unit">%</span></div>
          <div className="metric-label">System Uptime</div>
        </div>
        <div className="metrics-cell">
          <div className="metric-value">12 <span className="metric-unit">ms</span></div>
          <div className="metric-label">Avg p99 Latency</div>
        </div>
        <div className="metrics-cell">
          <div className="metric-value">340 <span className="metric-unit"></span></div>
          <div className="metric-label">Active Deployments</div>
        </div>
      </section>

      {/* Event Stream Table */}
      <section className="event-stream">
        <div style={{marginBottom: '24px', display: 'flex', gap: '16px', alignItems: 'center'}}>
          <h2 className="headline-fluid" style={{fontSize: '24px', maxWidth: 'none'}}>Trace: <span className="data-mono" style={{color: '#fff'}}>req-9f82d1c</span></h2>
          <Chip status="pass" text="SUCCESS" />
          <div className="data-mono">1.24s total</div>
        </div>

        <div className="event-layout">
          <div className="event-sidebar">
            <div className="sidebar-item active"><div className="chip-dot pass"></div> auth.verify_token</div>
            <div className="sidebar-item"><div className="chip-dot pass"></div> db.query_user</div>
            <div className="sidebar-item"><div className="chip-dot warn"></div> cache.miss</div>
            <div className="sidebar-item"><div className="chip-dot fail"></div> api.fetch_profile</div>
            <div className="sidebar-item"><div className="chip-dot pass"></div> queue.publish</div>
          </div>
          <div className="event-main">
            <div className="event-header data-mono" style={{fontSize: '12px'}}>
              <div className="col-span">SPAN</div>
              <div className="col-start">START</div>
              <div className="col-duration">DURATION</div>
            </div>
            <div className="event-row data-mono">
              <div className="col-span">auth.verify</div>
              <div className="col-start">
                <TimelineBar startPercent={0} widthPercent={15} active={false} />
              </div>
              <div className="col-duration">145ms</div>
            </div>
            <div className="event-row data-mono">
              <div className="col-span">db.query</div>
              <div className="col-start">
                <TimelineBar startPercent={15} widthPercent={45} active={false} />
              </div>
              <div className="col-duration">560ms</div>
            </div>
            <div className="event-row data-mono">
              <div className="col-span" style={{color: '#52a8ff'}}>cache.miss</div>
              <div className="col-start">
                <TimelineBar startPercent={60} widthPercent={10} active={true} />
              </div>
              <div className="col-duration" style={{color: '#52a8ff'}}>80ms</div>
            </div>
            <div className="event-row data-mono">
              <div className="col-span" style={{color: '#ededed'}}>api.fetch</div>
              <div className="col-start">
                <TimelineBar startPercent={70} widthPercent={30} active={false} />
              </div>
              <div className="col-duration" style={{color: '#ededed'}}>410ms</div>
            </div>
          </div>
        </div>
      </section>

      {/* Bento Feature Grid */}
      <section className="bento-grid">
        <div className="tech-card">
          <h3 style={{marginBottom: '16px', fontWeight: 500}}>Regression Suite</h3>
          <div className="flex-col gap-4">
            <div className="flex justify-between items-center">
              <span className="data-mono" style={{fontSize: '14px'}}>core/auth_spec.rb</span>
              <Chip status="pass" text="PASS" />
            </div>
            <div className="flex justify-between items-center">
              <span className="data-mono" style={{fontSize: '14px'}}>api/billing_spec.rb</span>
              <Chip status="fail" text="FAIL (-2.4%)" />
            </div>
            <div className="flex justify-between items-center">
              <span className="data-mono" style={{fontSize: '14px'}}>workers/email.rb</span>
              <Chip status="warn" text="WARN" />
            </div>
          </div>
        </div>

        <div className="tech-card">
          <h3 style={{marginBottom: '16px', fontWeight: 500}}>Failure Clustering</h3>
          <div className="flex-col gap-4">
            <div>
              <div className="flex justify-between data-mono" style={{fontSize: '12px', marginBottom: '8px'}}>
                <span>NetworkTimeoutError</span>
                <span>45%</span>
              </div>
              <div style={{width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)'}}>
                <div style={{width: '45%', height: '100%', background: '#ededed'}}></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between data-mono" style={{fontSize: '12px', marginBottom: '8px'}}>
                <span>ValidationException</span>
                <span>30%</span>
              </div>
              <div style={{width: '100%', height: '8px', background: 'rgba(255,255,255,0.1)'}}>
                <div style={{width: '30%', height: '100%', background: '#52a8ff'}}></div>
              </div>
            </div>
          </div>
        </div>

        <div className="tech-card" style={{position: 'relative', overflow: 'hidden'}}>
          <h3 style={{marginBottom: '16px', fontWeight: 500}}>Version Replay</h3>
          <div className="data-mono" style={{fontSize: '12px', background: '#050505', padding: '12px', borderLeft: '2px solid #52a8ff'}}>
            <div style={{color: '#999'}}>- config.timeout = 30</div>
            <div style={{color: '#fff'}}>+ config.timeout = 60</div>
            <br/>
            <div style={{color: '#999'}}>- await client.connect()</div>
            <div style={{color: '#fff'}}>+ await client.connect(retry=3)</div>
          </div>
          <div style={{position: 'absolute', bottom: '-40px', right: '-40px', width: '150px', height: '150px', background: 'radial-gradient(circle, rgba(82, 168, 255, 0.15) 0%, rgba(0,0,0,0) 70%)'}}></div>
        </div>
      </section>

    </div>
  )
}

export default App
