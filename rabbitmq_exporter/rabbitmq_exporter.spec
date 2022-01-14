%global debug_package %{nil}

Name:    rabbitmq_exporter
Version: 0.28.0
Release: 1%{?dist}
Summary: Prometheus exporter for RabbitMQ metrics
License: MIT
URL:     https://github.com/kbudde/%{name}

Source0: https://github.com/kbudde/%{name}/releases/download/v%{version}/%{name}-%{version}.linux-amd64.tar.gz
Source1: %{name}.service
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

Prometheus exporter for RabbitMQ metrics.

%prep
%setup -q -n %{name}-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}

%pre
#getent group prometheus >/dev/null || groupadd -r prometheus
#getent passwd prometheus >/dev/null || \
#  useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin \
#          -c "Prometheus services" prometheus
#exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,prometheus,prometheus,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, prometheus, prometheus)%{_sharedstatedir}/prometheus
