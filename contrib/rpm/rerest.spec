%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           rerest
Version:        0.0.1
Release:        1%{?dist}
Summary:        Simple REST Api for release automation

License:        AGPLv3+
URL:            https://github.com/RHInception/re-rest
Source0:        rerest-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel, python-pip
Requires:       python-flask>=0.9, python-pika>=0.9.12, python-pymongo, python-blinker


%description
Simple REST Api for release automation.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_datarootdir}/rerest/{mod_wsgi,test-ca-script}/
cp -rf contrib/mod_wsgi/* $RPM_BUILD_ROOT/%{_datarootdir}/rerest/mod_wsgi/


%files
%doc README.md LICENSE AUTHORS
%{python_sitelib}/*
%{_datarootdir}/rerest/*


%changelog
* Tue Apr  8 2014 Steve Milner <stevem@gnulinux.net>- 0.0.1-1
- Initial spec
