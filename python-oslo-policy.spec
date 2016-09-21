%global pypi_name oslo.policy
%global pkg_name oslo-policy

%if 0%{?fedora} >=24
%global with_python3 1
%endif

Name:           python-%{pkg_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack oslo.policy library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description
An OpenStack library for policy.

%package -n python2-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
# test dependencies
BuildRequires:  python-hacking
BuildRequires:  python-oslotest
BuildRequires:  python-requests-mock
BuildRequires:  python-coverage
BuildRequires:  python-fixtures
BuildRequires:  python-mock
BuildRequires:  python-requests
BuildRequires:  PyYAML >= 3.1.0
# Required to compile translation files
BuildRequires:  python-babel

Requires:       python-oslo-config >= 2.3.0
Requires:       python-oslo-i18n >= 1.5.0
Requires:       python-oslo-serialization >= 1.4.0
Requires:       python-oslo-utils >= 2.0.0
Requires:       python-six >= 1.9.0
Requires:       PyYAML >= 3.1.0
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python2-%{pkg_name}
An OpenStack library for policy.

%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo policy library

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-i18n

%description -n python-%{pkg_name}-doc
Documentation for the Oslo policy library.

%package -n python-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library

Requires:  python-%{pkg_name} = %{version}-%{release}
Requires:  python-hacking
Requires:  python-oslotest
Requires:  python-requests-mock
Requires:  python-coverage
Requires:  python-fixtures
Requires:  python-mock
Requires:  python-requests

%description -n python-%{pkg_name}-tests
Test subpackage for the Oslo policy library

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.policy library
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# test dependencies
BuildRequires:  python3-hacking
BuildRequires:  python3-oslotest
BuildRequires:  python3-requests-mock
BuildRequires:  python3-coverage
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-requests
BuildRequires:  python3-PyYAML >= 3.1.0

Requires:       python3-oslo-config >= 2.3.0
Requires:       python3-oslo-i18n >= 1.5.0
Requires:       python3-oslo-serialization >= 1.4.0
Requires:       python3-oslo-utils >= 2.0.0
Requires:       python3-six >= 1.9.0
Requires:       python3-PyYAML >= 3.1.0
Requires:       python-%{pkg_name}-lang = %{version}-%{release}

%description -n python3-%{pkg_name}
An OpenStack library for policy.
%endif

%if 0%{?with_python3}
%package -n python3-%{pkg_name}-tests
Summary:    Test subpackage for the Oslo policy library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-hacking
Requires:  python3-oslotest
Requires:  python3-requests-mock
Requires:  python3-coverage
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-requests

%description -n python3-%{pkg_name}-tests
Test subpackage for the Oslo policy library
%endif

%package  -n python-%{pkg_name}-lang
Summary:   Translation files for Oslo policy library

%description -n python-%{pkg_name}-lang
Translation files for Oslo policy library

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -f requirements.txt

# FIXME (jpena): Remove buggy PO-Revision-Date lines in translation
# See https://bugs.launchpad.net/openstack-i18n/+bug/1586041 for details
sed -i '/^\"PO-Revision-Date: \\n\"/d' oslo_policy/locale/*/LC_MESSAGES/*.po

%build
%py2_build

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/oslo_policy/locale

%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif

%py2_install

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/oslo_policy/locale/*/LC_*/oslo_policy*po
rm -f %{buildroot}%{python2_sitelib}/oslo_policy/locale/*pot
mv %{buildroot}%{python2_sitelib}/oslo_policy/locale %{buildroot}%{_datadir}/locale
%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/oslo_policy/locale
%endif

# Find language files
%find_lang oslo_policy --all-name

%check
# Due to old version of python-fixtures, one test is failing
# so we are skipping the tests
%{__python2} setup.py test ||
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test ||
%endif

%files -n python2-%{pkg_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslopolicy-checker
%{_bindir}/oslopolicy-list-redundant
%{_bindir}/oslopolicy-policy-generator
%{_bindir}/oslopolicy-sample-generator
%{python2_sitelib}/oslo_policy
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/oslo_policy/tests

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%files -n python-%{pkg_name}-tests
%{python2_sitelib}/oslo_policy/tests

%files -n python-%{pkg_name}-lang -f oslo_policy.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_policy
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_policy/tests
%endif

%if 0%{?with_python3}
%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_policy/tests
%endif

%changelog
