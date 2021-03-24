#############################
# AUTOGENERATED FROM TEMPLATE
#############################
%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name:    jiralert
Version: 1.0
Release: 1%{?dist}
Summary: Prometheus Alertmanager webhook receiver for JIRA
License: ASL 2.0
URL:     https://github.com/prometheus-community/jiralert

Source0: https://github.com/prometheus-community/jiralert/releases/download/%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default
Source3: %{name}.yml
Source4: %{name}.tmpl

%{?systemd_requires}
Requires(pre): shadow-utils

%description
JIRAlert implements Alertmanager's webhook HTTP API and connects to one or more JIRA instances to create highly configurable JIRA issues. 



%prep
%setup -q -n %{name}-%{version}.linux-amd64


%build
/bin/true


%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
mkdir -vp %{buildroot}%{_sysconfdir}/prometheus/%{name}
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}/%{name}.yml
install -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/prometheus/%{name}/%{name}.tmpl

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus
exit 0


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %{_sysconfdir}/prometheus/%{name}
%config(noreplace) %attr(644, root, root)%{_sysconfdir}/prometheus/%{name}/%{name}.yml
%config(noreplace) %attr(644, root, root)%{_sysconfdir}/prometheus/%{name}/%{name}.tmpl
