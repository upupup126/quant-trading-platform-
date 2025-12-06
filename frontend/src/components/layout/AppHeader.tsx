import React from 'react'
import { Layout, Menu, Avatar, Dropdown, Badge } from 'antd'
import {
  BellOutlined,
  UserOutlined,
  SettingOutlined,
  LogoutOutlined
} from '@ant-design/icons'
import { Link, useLocation } from 'react-router-dom'
import './AppHeader.css'

const { Header } = Layout

const AppHeader: React.FC = () => {
  const location = useLocation()
  
  const menuItems = [
    {
      key: '/market',
      label: <Link to="/market">行情中心</Link>,
      icon: null
    },
    {
      key: '/strategy',
      label: <Link to="/strategy">策略管理</Link>,
      icon: null
    },
    {
      key: '/trade',
      label: <Link to="/trade">交易终端</Link>,
      icon: null
    },
    {
      key: '/portfolio',
      label: <Link to="/portfolio">资产监控</Link>,
      icon: null
    }
  ]
  
  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人资料'
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '系统设置'
    },
    {
      type: 'divider'
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录'
    }
  ]
  
  const selectedKey = menuItems.find(item => 
    location.pathname.startsWith(item.key)
  )?.key || '/market'
  
  const userMenu = {
    items: userMenuItems,
    onClick: (e: any) => {
      console.log('User menu click:', e.key)
      if (e.key === 'logout') {
        // 处理退出登录
        console.log('Logout clicked')
      }
    }
  }
  
  return (
    <Header className="app-header">
      <div className="header-left">
        <div className="logo-container">
          <div className="logo">
            <span className="logo-text">量化交易平台</span>
          </div>
        </div>
        <Menu
          mode="horizontal"
          selectedKeys={[selectedKey]}
          items={menuItems}
          className="main-menu"
        />
      </div>
      
      <div className="header-right">
        <div className="header-actions">
          <Badge count={5} className="notification-badge">
            <BellOutlined className="notification-icon" />
          </Badge>
          
          <Dropdown menu={userMenu} placement="bottomRight" arrow>
            <div className="user-info">
              <Avatar 
                icon={<UserOutlined />} 
                className="user-avatar"
              />
              <span className="username">管理员</span>
            </div>
          </Dropdown>
        </div>
      </div>
    </Header>
  )
}

export default AppHeader