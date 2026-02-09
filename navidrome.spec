Name:           navidrome
Version:        0.60.2
Release:        1%{?dist}
Summary:        Modern Music Server and Streamer compatible with Subsonic/Airsonic 

License:        GPLv3
URL:            https://www.navidrome.org/
Source0:        https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-v%{version}.tar.gz
Source1:        navidrome.service
Source2:        navidrome.sysusers
Source3:        navidrome.toml

Patch0:         0001-Fix-Makefile-for-packaging.patch
Patch1:         0002-Fix-about-version-number-for-packaging.patch

BuildRequires:  git
BuildRequires:  golang >= 1.21
BuildRequires:  nodejs24
BuildRequires:  nodejs24-npm
BuildRequires:  taglib-devel, zlib-devel, zlib
BuildRequires:  make, gcc, gcc-c++
BuildRequires:  systemd-units
BuildRequires:  systemd-rpm-macros
%{?sysusers_requires_compat}

Requires: systemd-units
Requires: zlib
Requires: ffmpeg
Requires: taglib

%description

Navidrome is an open source web-based music collection server and streamer. 
It gives you freedom to listen to your music collection from any browser 
or mobile device.

%global debug_package %{nil}

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
export NODE_OPTIONS="--max-old-space-size=8192"
export GOTOOLCHAIN="auto"
export GOSUMDB="sum.golang.org"
make setup GIT_TAG="%{version}-%{release}"
make build GIT_TAG="%{version}-%{release}"

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/data
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}/music
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

install -p -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.toml

%pre
%sysusers_create_compat %{SOURCE2}

%files
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.toml
%dir %{_sharedstatedir}/%{name}

%changelog
