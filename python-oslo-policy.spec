%global pypi_name oslo.policy

Name:           python-oslo-policy
Version:        0.3.2
Release:        1%{?dist}
Summary:        OpenStack Oslo Policy library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
# for docs build
BuildRequires:  python-oslo-config >= 1.9.0
BuildRequires:  python-oslo-i18n >= 1.3.0
BuildRequires:  python-oslo-serialization >= 1.2.0

Requires:       python-oslo-config >= 1.9.0
Requires:       python-oslo-i18n >= 1.3.0
Requires:       python-oslo-serialization >= 1.2.0

%description
The OpenStack Oslo Policy library.
RBAC policy enforcement library for OpenStack.

%package doc
Summary:    Documentation for the Oslo Policy library
Group:      Documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for the Oslo Policy library.

%prep
%setup -q -n %{pypi_name}-%{version}
# Let RPM handle the dependencies
rm -f requirements.txt

%build
%{__python2} setup.py build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

#delete tests
rm -fr %{buildroot}%{python2_sitelib}/%{pypi_name}/tests/

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.rst
%{python2_sitelib}/oslo_policy
%{python2_sitelib}/*.egg-info

%files doc
%license LICENSE
%doc html

%changelog
* Wed Jun 17 2015 Alan Pevec <alan.pevec@redhat.com> 0.3.2-1
- Update to upstream 0.3.2

* Sat Mar 7 2015 Dan Prince <dprince@redhat.com> - 0.3.1-1
- Initial package
